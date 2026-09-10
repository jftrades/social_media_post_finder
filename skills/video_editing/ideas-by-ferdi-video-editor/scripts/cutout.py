# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy==2.2.6", "onnxruntime==1.23.2"]
# ///
"""Local RVM alpha cache. Run with uv; no video uploads or automatic model downloads."""
import argparse
from pathlib import Path
import subprocess
import time
import numpy as np
import onnxruntime as ort
import video as v

MODEL = v.TOOLS/'RobustVideoMatting'/'rvm_mobilenetv3_fp32.onnx'
MODEL_SHA256 = '88d4531297118f595bf2fd60f6f566aec2e559393802d1f436c380f0cbbd2828'


def boundaries(plan):
    offset=0.;cuts={0}
    for s in plan['segments']:
        cuts.add(round(offset*30))
        offset+=s['end']-s['start']
    return cuts


def make_alpha(source,plan,work):
    if not MODEL.is_file():
        raise ValueError('Install the documented RVM ONNX model in agent_tooling/RobustVideoMatting first.')
    if v.digest(MODEL)!=MODEL_SHA256:
        raise ValueError('Unexpected RVM model checksum')
    width,height,fps=1080,1920,30
    broll=[(b['at'],b['at']+b['end']-b['start']) for b in plan['job'].get('broll',[])]
    cuts=boundaries(plan)
    key=dict(source_sha256=v.digest(source),model_sha256=MODEL_SHA256,cuts=sorted(cuts),
             broll=broll,width=width,height=height,fps=fps,downsample_ratio=.25,version=1)
    # JSON converts tuples to lists; normalize before comparison.
    key['broll']=[list(x) for x in broll]
    target=work/'cutout-alpha.mkv';stamp=work/'cutout-cache.json'
    if target.exists() and stamp.exists():
        cached=v.read(stamp)
        if cached.get('key')==key and cached.get('sha256')==v.digest(target):
            print('RVM: reusing verified alpha cache',flush=True)
            return target
    opts=ort.SessionOptions();opts.intra_op_num_threads=4;opts.inter_op_num_threads=1
    session=ort.InferenceSession(str(MODEL),sess_options=opts,providers=['CPUExecutionProvider'])
    ratio=np.array([.25],dtype=np.float32)
    rec=[np.zeros((1,1,1,1),dtype=np.float32) for _ in range(4)]
    partial=work/'cutout-alpha.partial.mkv'
    started=time.monotonic();count=0;was_active=False;reset_frames=[]
    with (work/'cutout-decode.log').open('wb') as dec_log,(work/'cutout-encode.log').open('wb') as enc_log:
        decoder=subprocess.Popen([str(v.FF),'-v','error','-i',str(source),'-map','0:v:0','-an',
            '-vf',f'scale={width}:{height},fps={fps}','-pix_fmt','rgb24','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE,stderr=dec_log)
        encoder=subprocess.Popen([str(v.FF),'-v','error','-y','-f','rawvideo','-pix_fmt','gray',
            '-s',f'{width}x{height}','-r',str(fps),'-i','pipe:0','-an','-c:v','ffv1','-level','3',
            '-pix_fmt','gray',str(partial)],stdin=subprocess.PIPE,stderr=enc_log)
        try:
            while True:
                data=decoder.stdout.read(width*height*3)
                if not data:break
                if len(data)!=width*height*3:raise ValueError('Incomplete decoded frame')
                t=count/fps
                active=not any(a<=t<b for a,b in broll)
                if active:
                    if count in cuts or not was_active:
                        rec=[np.zeros((1,1,1,1),dtype=np.float32) for _ in range(4)]
                        reset_frames.append(count)
                    src=np.frombuffer(data,dtype=np.uint8).reshape(height,width,3)
                    src=np.ascontiguousarray(src.transpose(2,0,1)[None],dtype=np.float32)/255
                    _,alpha,*rec=session.run(None,dict(src=src,r1i=rec[0],r2i=rec[1],r3i=rec[2],r4i=rec[3],downsample_ratio=ratio))
                    if not np.isfinite(alpha).all():raise ValueError('Invalid RVM alpha output')
                    mask=np.rint(np.clip(alpha[0,0],0,1)*255).astype(np.uint8)
                else:
                    mask=np.zeros((height,width),dtype=np.uint8)
                encoder.stdin.write(mask.tobytes())
                was_active=active;count+=1
                if count%30==0:print(f'RVM: {count/fps:.0f}s video / {time.monotonic()-started:.1f}s elapsed',flush=True)
            decoder.stdout.close();encoder.stdin.close()
            if decoder.wait()!=0 or encoder.wait()!=0:raise ValueError('FFmpeg cutout pipe failed; inspect cutout logs')
            if abs(count/fps-plan['duration'])>.25:raise ValueError('Alpha frame count differs from edit duration')
            v.ff(['-v','error','-i',partial,'-f','null','-'])
            partial.replace(target)
            v.save(stamp,dict(key=key,frames=count,reset_frames=reset_frames,seconds=time.monotonic()-started,sha256=v.digest(target)))
        finally:
            for proc in (decoder,encoder):
                if proc.poll() is None:proc.kill();proc.wait()
    print(f'RVM: {count} frames verified, alpha saved',flush=True)
    return target


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source',type=Path)
    parser.add_argument('plan',type=Path)
    args=parser.parse_args()
    plan=v.read(args.plan)
    v.cutout_gate(plan['job'])
    if plan['job'].get('title_behind_person') is not True or plan.get('reviewed') is not True:
        raise ValueError('Cutout requires opt-in and a reviewed plan')
    make_alpha(args.source.resolve(),plan,args.plan.resolve().parent)
