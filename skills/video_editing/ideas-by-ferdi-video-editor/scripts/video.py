# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow==12.3.0"]
# ///
"""Small local editor. Commands: prepare, plan, render, finish. Run with uv."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PROJECTS = ROOT / 'project_videos'
TOOLS = ROOT / 'agent_tooling'
WHISPER = TOOLS / 'Purfview-Faster-Whisper-XXL'
FF = WHISPER / 'ffmpeg.exe'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def run(args, cwd=None):
    p = subprocess.run([str(x) for x in args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode:
        raise RuntimeError(p.stderr[-6000:] or p.stdout[-6000:])
    return p.stderr + p.stdout


def ff(args, cwd=None):
    return run([FF, '-hide_banner', '-y', *args], cwd)


def media(value):
    p = Path(value)
    p = (ROOT / p).resolve() if not p.is_absolute() else p.resolve()
    if not p.is_file():
        raise ValueError(f'Missing media: {p}')
    return p


def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def duration(path):
    s = ff(['-i', path, '-t', '0', '-f', 'null', '-'])
    m = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', s)
    if not m:
        raise ValueError(f'No duration: {path}')
    return int(m[1])*3600 + int(m[2])*60 + float(m[3])


def gate(job):
    mode=job.get('mode')
    if mode not in ('single', 'multi', 'voiceover'):
        raise ValueError('Invalid mode')
    required=('format','clips','captions','music','title','broll','capture','audio_normalization','zooms')
    required+=('original_audio','visual_timing','retiming','broll_fallback') if mode=='voiceover' else ('cleanup',)
    if job.get('intake_confirmed') is not True or job.get('intake_completed_levels') != [1,2,3] or not all(job.get('intake', {}).get(k) for k in required):
        raise ValueError('Complete intake levels 1, 2 and 3 in order before editing.')
    if job['intake']['audio_normalization'] not in ('ja','nein') or job.get('audio_normalize') is not (job['intake']['audio_normalization']=='ja'):
        raise ValueError('Audio normalization needs an explicit matching yes/no answer.')
    if job.get('title') and (not isinstance(job.get('title_duration'),(int,float)) or not math.isfinite(job['title_duration']) or job['title_duration'] <= 0):
        raise ValueError('Ask title duration in seconds.')
    if job.get('segment_overrides'):
        raise ValueError('Segment exceptions need an explicitly adapted render plan; do not silently apply global defaults.')
    if mode == 'voiceover':
        if len(job.get('sources',[])) != 1:
            raise ValueError('Voice-over requires exactly one narration source.')
        if job.get('visual_cut_policy') != 'one_second_montage_over_5s' or job['intake']['visual_timing'] != job['visual_cut_policy']:
            raise ValueError('Voice-over must use the confirmed one-second montage policy for clips over five seconds.')
        policy=job.get('voiceover_broll_policy')
        if policy not in ('none','explicit','if_insufficient','explicit_or_insufficient') or job['intake']['broll_fallback'] != policy:
            raise ValueError('Confirm when extra B-roll may be used.')
        if policy != 'none' and not job.get('broll_allowed'):
            raise ValueError('Name the B-roll folders allowed for fallback.')
        answer=job['intake']['original_audio']
        inserts=job.get('voiceover_inserts')
        if answer not in ('ja','nein') or not isinstance(inserts,list) or (answer=='ja') is not bool(inserts):
            raise ValueError('Confirm original-audio inserts and document each approved insert.')
        for insert in inserts:
            if not isinstance(insert,dict) or not all(k in insert for k in ('path','start','end','reason')):
                raise ValueError('Each original-audio insert needs path, start, end and reason.')
            start,end=insert['start'],insert['end']
            if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in (start,end)) or not 0 <= start < end or not str(insert['reason']).strip():
                raise ValueError('Each original-audio insert needs a valid interval and spoken-line description.')
    zoom_gate(job)
    title_gate(job)
    cutout_gate(job)
    if job.get('capture') not in ('phone', 'camera', 'graded'):
        raise ValueError('Choose phone, camera or graded capture.')
    if job.get('broll_mode') not in ('none', 'specific', 'selected', 'auto'):
        raise ValueError('Choose a B-roll mode.')
    if job.get('broll_mode') == 'none' and job.get('broll'):
        raise ValueError('B-roll is disabled.')
    if 'title' not in job or not isinstance(job['title'], str):
        raise ValueError('Set title text, or an empty string for no title.')
    if not re.fullmatch(r'[\w-]+', job['project']):
        raise ValueError('Project name must contain only letters, numbers, hyphens or underscores.')
    if not job['sources'] or (mode == 'single' and len(job['sources']) != 1):
        raise ValueError('Invalid source count')


def prepare(job, work):
    target = work / 'transcripts'
    target.mkdir(exist_ok=True)
    for i, source in enumerate(job['sources']):
        src = media(source)
        folder = target / str(i)
        folder.mkdir(exist_ok=True)
        stamp = {'source': str(src), 'sha256': digest(src), 'model': 'medium', 'language': 'de'}
        cache = folder / 'source.json'
        if cache.exists() and read(cache) == stamp and (folder / 'speech.json').exists():
            continue
        wav = folder / 'speech.wav'
        ff(['-i', src, '-vn', '-ac', '1', '-ar', '16000', wav])
        run([WHISPER / 'faster-whisper-xxl.exe', wav, '--model', 'medium', '--model_dir', WHISPER / '_models',
             '--language', 'de', '--device', 'cpu', '--compute_type', 'int8', '--word_timestamps', 'True',
             '--one_word', '0', '--sentence', '--max_line_width', '14', '--max_line_count', '1',
             '--output_dir', folder, '--output_format', 'json', 'srt'])
        if not (folder / 'speech.json').exists():
            raise ValueError('Purfview produced no expected JSON transcript')
        save(cache, stamp)


def words_for(work, i):
    data = read(work / 'transcripts' / str(i) / 'speech.json')
    words = [dict(w) for s in data['segments'] for w in s.get('words', [])]
    if not words:
        raise ValueError('No word timestamps. Rerun local transcription.')
    for w in words:
        w['word'] = w['word'].strip()
        if not (math.isfinite(w['start']) and math.isfinite(w['end']) and 0 <= w['start'] <= w['end']):
            raise ValueError('Invalid word timestamp')
    return sorted(words, key=lambda w: w['start'])


def plan(job, work):
    zoom_gate(job)
    segments, output_words, offset = [], [], 0.0
    for i, source in enumerate(job['sources']):
        words = words_for(work, i)
        length = duration(media(source))
        drops = [d for d in job.get('drops', []) if d['source'] == i] if job['cleanup'] else []
        kept = [w for w in words if not any(w['start'] < d['end'] and (w['end'] > d['start'] or d['start'] <= w['start'] < d['end']) for d in drops)]
        if not kept:
            continue
        intervals = []
        if job['cleanup']:
            for w in kept:
                start, end = max(0, w['start']-.06), min(length, w['end']+.10)
                if intervals and start-intervals[-1][1] <= .29 and not any(d['start'] < start and d['end'] > intervals[-1][1] for d in drops):
                    intervals[-1][1] = max(intervals[-1][1], end)
                else:
                    intervals.append([start, end])
        else:
            intervals = [[0, length]]
        # Protect only explicitly selected short breaths, not every pause.
        for z in job.get('zooms', []):
            if z['source'] != i:
                continue
            if any(d['start'] < z['end'] and d['end'] > z['start'] for d in drops):
                raise ValueError('Zoom breath overlaps a discarded take')
            intervals.append([z['start'], z['end']])
        merged = []
        for start, end in sorted(intervals):
            if merged and start <= merged[-1][1]+.00001:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start,end])
        intervals = merged
        for start, end in intervals:
            segments.append({'source': i, 'start': start, 'end': end})
            for w in kept:
                if start <= w['start'] and w['end'] <= end:
                    output_words.append({'word': w['word'], 'start': offset+w['start']-start, 'end': offset+w['end']-start})
            offset += end-start
    if not segments:
        raise ValueError('Empty edit')
    events = zoom_timeline(job, segments)
    save(work / 'plan.json', {'reviewed': False, 'job': job, 'segments': segments, 'words': output_words, 'duration': offset, 'zooms': events})


def zoom_gate(job):
    if job['mode'] in ('single','multi','voiceover'):
        answer = job.get('intake', {}).get('zooms')
        if answer not in ('ja','nein') or job.get('zoom_enabled') is not (answer == 'ja'):
            raise ValueError('Ask level 2 effects: zooms ja/nein; set zoom_enabled to match.')
    if job.get('zooms') and job.get('zoom_enabled') is not True:
        raise ValueError('Zooms need explicit opt-in')
    for z in job.get('zooms', []):
        if not isinstance(z['source'],int) or not 0 <= z['source'] < len(job['sources']):
            raise ValueError('Invalid zoom source')
        values = [z['start'],z['end'],z['reset'],z.get('out_duration',0)]
        if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in values):
            raise ValueError('Invalid zoom times')
        if not (0 <= z['start'] < z['end'] <= z['reset'] and .1 <= z['end']-z['start'] <= .9
                and (z.get('out_duration',0) == 0 or .1 <= z['out_duration'] <= .9)) or not z.get('reason'):
            raise ValueError('Zoom needs a short 0.1–0.9s breath, reset and reason')


def zoom_timeline(job, segments):
    events = []
    for z in job.get('zooms', []):
        offset = 0
        for s in segments:
            if s['source'] == z['source'] and s['start'] <= z['start'] and z['end'] <= s['end']+.00001:
                # Never carry the 120% framing across an edit/angle boundary.
                reset = min(z['reset'],s['end'])
                out = min(z.get('out_duration',0),max(0,s['end']-reset))
                events.append(dict(start=offset+z['start']-s['start'],end=offset+z['end']-s['start'],
                                   reset=offset+reset-s['start'],out_duration=out,reason=z['reason']))
                break
            offset += s['end']-s['start']
        else:
            raise ValueError('Zoom breath must connect to its kept spoken passage')
    events.sort(key=lambda z:z['start'])
    if job['mode'] == 'voiceover' and events:
        boundaries=[]
        total=0
        for visual in job.get('visuals',[]):
            total+=(visual['end']-visual['start'])/visual.get('speed',1)
            boundaries.append(total)
        for event in events:
            boundary=next((t for t in boundaries if t > event['start']+1e-5),None)
            if boundary is None or event['end'] > boundary+1e-5:
                raise ValueError('Voice-over zoom must fit within one visual; complete visuals before planning zooms.')
            event['reset']=min(event['reset'],boundary)
            event['out_duration']=min(event['out_duration'],boundary-event['reset'])
    previous_end = 0
    for z in events:
        if z['start'] < previous_end-.00001:
            raise ValueError('Overlapping zooms: return to 100% before another zoom')
        previous_end = z['reset']+z['out_duration']
        if any(b['at'] < previous_end and b['at']+b['end']-b['start'] > z['start'] for b in job.get('broll',[])):
            raise ValueError('Move zooms outside B-roll overlays')
    return events


def zoom_filter(events):
    expression = '1'
    for z in reversed(events):
        a,b,r,d = z['start'],z['end'],z['reset'],z['out_duration']
        t = f'((on/30-{a})/{b-a})'
        ramp = f'(1+0.2*{t}*{t}*(3-2*{t}))'
        tail = expression
        if d:
            u = f'((on/30-{r})/{d})'
            tail = f'if(lt(on/30,{r+d}),1.2-0.2*{u}*{u}*(3-2*{u}),{expression})'
        expression = f'if(lt(on/30,{a}),{expression},if(lt(on/30,{b}),{ramp},if(lt(on/30,{r}),1.2,{tail})))'
    return f"zoompan=z='{expression}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30"


def zoom_audio(events, work, length):
    sounds = [(z['start'],z['end']-z['start']) for z in events]
    sounds += [(z['reset'],z['out_duration']) for z in events if z['out_duration']]
    effect = media('agent_tooling/sound_fx/whoosh-swift-cut-jam-fx-1-00-00.mp3')
    ratio = 2**(-2/12)
    graph = [f'[1:a]aresample=48000,asetrate={48000*ratio},aresample=48000,atempo={1/ratio},volume=-6dB,asplit={len(sounds)}'+''.join(f'[s{i}]' for i in range(len(sounds)))]
    for i,(at,d) in enumerate(sounds):
        graph.append(f'[s{i}]apad,atrim=duration={d},afade=t=in:d=0.015,afade=t=out:st={max(0,d-.04)}:d=0.04,adelay={round(at*48000)}S:all=1[e{i}]')
    graph.append('[0:a]'+''.join(f'[e{i}]' for i in range(len(sounds)))+f'amix=inputs={len(sounds)+1}:duration=first:normalize=0[a]')
    ff(['-f','lavfi','-i',f'anullsrc=r=48000:cl=stereo:d={length}','-i',effect,
        '-filter_complex',';'.join(graph),'-map','[a]','-c:a','pcm_s16le','zoom-sfx.wav'],work)


def ass_time(t):
    n = round(t*100)
    return f'{n//360000}:{n//6000%60:02}:{n//100%60:02}.{n%100:02}'


def captions(job, words, work):
    header = '[Script Info]\nPlayResX: 1080\nPlayResY: 1920\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
    header += f"Style: Default,{job.get('font', 'Alte Haas Grotesk')},{job.get('font_size',58)},&H00FFFFFF,&H00FFFFFF,&H90000000,&H90000000,-1,0,0,0,100,100,-1,0,1,0,0,5,80,80,0,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    groups = []
    for w in (words if job.get('captions') else []):
        if groups and len(groups[-1]) < 3 and len(' '.join(x['word'] for x in groups[-1])+' '+w['word']) <= 14 and w['start']-groups[-1][-1]['end'] < .3 and not re.search(r'[.!?]$', groups[-1][-1]['word']):
            groups[-1].append(w)
        else:
            groups.append([w])
    def add_text(text, start, end, y, font, size, bold, spacing, anchor=5):
        nonlocal header
        text = text.replace('\\', '').replace('{', '').replace('}', '').replace('\n', r'\N')
        common = f'\\an{anchor}\\pos(540,{y})\\fn{font}\\fs{size}\\b{bold}\\fsp{spacing}'
        # Separate shadow layer: blurred black glyphs below sharp white text.
        for layer, effect in ((0, r'\1c&H000000&\1a&H75&\bord1\3c&H000000&\3a&H75&\shad0\blur5'),
                              (1, r'\1c&HFFFFFF&\1a&H00&\bord0\shad0\blur0')):
            pos = common if layer else common.replace(f'540,{y}', f'541,{y+3}')
            header += f'Dialogue: {layer},{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{{{pos}{effect}}}{text}\n'
    for g in groups:
        add_text(' '.join(w['word'] for w in g), g[0]['start'], g[-1]['end'],
                 job.get('caption_y',1200), job.get('font','Alte Haas Grotesk'),
                 job.get('font_size',58), 1, -1)
    if job.get('title'):
        title_image(job, work)
    (work / 'captions.ass').write_text(header, encoding='utf-8')



STATIC_TITLE_STYLES = ('snapchat', 'max_readable')
MULTILINE_TITLE_STYLES = ('preset_1', 'preset_2', 'preset_3')
TITLE_STYLES = STATIC_TITLE_STYLES + MULTILINE_TITLE_STYLES
EMPTY_TITLE_LINES = ('', 'nix', 'leer', 'kein text')


def title_lines(job):
    values=job.get('title_lines')
    if not isinstance(values,list) or len(values)!=3 or not all(isinstance(x,str) for x in values):
        raise ValueError('Preset 1/2/3 require exactly three text answers: oben, mitte, unten.')
    return ['' if x.strip().casefold() in EMPTY_TITLE_LINES else x.strip() for x in values]


def title_gate(job):
    style = job.get('title_style', 'max_readable')
    if style not in TITLE_STYLES:
        raise ValueError('Unknown title style')
    if style in MULTILINE_TITLE_STYLES:
        lines=title_lines(job)
        combined='\n'.join(x for x in lines if x)
        if job.get('title','').strip() != combined:
            raise ValueError('Preset title must equal its non-empty oben/mitte/unten lines in order.')
    if job.get('title'):
        if job.get('intake',{}).get('title_style') != style:
            raise ValueError('Ask title style: Snapchat / Max-Readable / Preset 1 / Preset 2 / Preset 3')


def cutout_gate(job):
    enabled=job.get('title_behind_person',False)
    if not isinstance(enabled,bool):
        raise ValueError('title_behind_person must be true or false')
    if job.get('title') and job['mode'] in ('single','multi'):
        answer=job.get('intake',{}).get('cutout')
        if answer not in ('ja','nein') or enabled is not (answer=='ja'):
            raise ValueError('Ask level 3: title behind person ja/nein')
    elif enabled:
        raise ValueError('Title cutout requires a title and single/multi talking-head footage')


def visual_filter(job,plan):
    """Keep captions above both the title and person; only picture layers are zoomed."""
    if not job.get('title'):
        return 'ass=captions.ass:fontsdir=fonts'
    end=float(job.get('title_duration',plan['duration']))
    if not math.isfinite(end) or end<=0:
        raise ValueError('Title duration must be positive and finite')
    if job.get('title_behind_person'):
        return ("split=2[background][person];movie=title.png[title];"
                f"[background][title]overlay=eof_action=repeat:enable='lt(t,{end})'[titled];"
                "movie=cutout-alpha.mkv,format=gray[alpha];"
                "[person][alpha]alphamerge[foreground];"
                "[titled][foreground]overlay=shortest=1,ass=captions.ass:fontsdir=fonts")
    return (f"movie=title.png[title];[in][title]overlay=eof_action=repeat:enable='lt(t,{end})',"
            'ass=captions.ass:fontsdir=fonts')


MULTILINE_TITLE_PRESETS = {
    'preset_1': (
        dict(slot='oben',font='AlteHaasGroteskBold.ttf',scale=.745,x=0,y=1288,spacing=-1,shadow=True),
        dict(slot='mitte',font='AlteHaasGroteskBold.ttf',scale=1.458,x=0,y=1136,spacing=-1,shadow=True),
        dict(slot='unten',font='Child Hood.otf',scale=.626,x=419,y=1020,spacing=0,shadow=True,star=True)),
    'preset_2': (
        dict(slot='oben',font='AlteHaasGroteskBold.ttf',scale=2.08,x=-316,y=1079,spacing=-1,shadow=True,stroke=3),
        dict(slot='mitte',font='AlteHaasGroteskBold.ttf',scale=2.08,x=280,y=872,spacing=-1,shadow=True,stroke=3),
        dict(slot='unten',font='Child Hood.otf',scale=.603,x=419,y=672,spacing=0,shadow=True,star=True)),
    'preset_3': (
        dict(slot='oben',font='AlteHaasGroteskBold.ttf',scale=.80,x=0,y=300,spacing=0,shadow=False),
        dict(slot='mitte',font='Tanker-Regular.otf',scale=2.376,x=0,y=120,spacing=-1,shadow=False),
        dict(slot='unten',font='Tanker-Regular.otf',scale=2.376,x=0,y=-120,spacing=-1,shadow=False))
}


def multiline_title_image(job,work):
    from PIL import Image,ImageDraw,ImageFont,ImageFilter
    style=job['title_style']
    lines=title_lines(job)
    canvas=Image.new('RGBA',(1080,1920))
    layout=[]
    for text,spec in zip(lines,MULTILINE_TITLE_PRESETS[style]):
        if not text:
            layout.append({**spec,'text':'','rendered':False})
            continue
        if spec.get('star') and not text.startswith('*'):
            text='*'+text
        size=round(15*4*spec['scale'])
        font=ImageFont.truetype(str(TOOLS/'fonts'/spec['font']),size)
        stroke=spec.get('stroke',0)
        advances=[font.getlength(char) for char in text]
        width=max(1,math.ceil(sum(advances)+spec['spacing']*max(0,len(text)-1)+2*stroke))
        boxes=[font.getbbox(char,stroke_width=stroke) for char in text]
        top=min(box[1] for box in boxes);bottom=max(box[3] for box in boxes)
        mask=Image.new('L',(width+12,max(1,bottom-top)+12))
        draw=ImageDraw.Draw(mask);x=6
        for char,advance in zip(text,advances):
            draw.text((x+stroke,6-top),char,font=font,fill=255,stroke_width=stroke,stroke_fill=255)
            x+=advance+spec['spacing']
        center_x=540+spec['x']/2
        center_y=960-spec['y']/2
        left=round(center_x-mask.width/2);upper=round(center_y-mask.height/2)
        if left<0 or upper<0 or left+mask.width>1080 or upper+mask.height>1920:
            raise ValueError(f"{style} {spec['slot']} text does not fit its fixed position; shorten the line.")
        if spec['shadow']:
            shadow=Image.new('L',canvas.size)
            shadow.paste(mask,(left+1,upper+3))
            shadow=shadow.filter(ImageFilter.GaussianBlur(4)).point(lambda value:round(value*.38))
            dark=Image.new('RGBA',canvas.size,(0,0,0,0));dark.putalpha(shadow)
            canvas=Image.alpha_composite(canvas,dark)
        alpha=Image.new('L',canvas.size);alpha.paste(mask,(left,upper))
        light=Image.new('RGBA',canvas.size,(255,255,255,0));light.putalpha(alpha)
        canvas=Image.alpha_composite(canvas,light)
        layout.append({**spec,'text':text,'rendered':True,'font_size_px':size,
                       'output_x':center_x,'output_y':center_y,'bounds':[left,upper,left+mask.width,upper+mask.height]})
    canvas.save(work/'title.png')
    save(work/'title-layout.json',{'style':style,'base_font_size':15,'coordinate_space':'2160x3840 center-origin; rendered at 50%',
                                   'animation':'pending design approval','lines':layout})


def title_image(job, work):
    from PIL import Image, ImageDraw, ImageFont
    style = job.get('title_style','max_readable')
    if style not in TITLE_STYLES:
        raise ValueError('Unknown title style')
    if style in MULTILINE_TITLE_STYLES:
        return multiline_title_image(job,work)
    path = TOOLS/'fonts'/('LiberationSans-Regular.ttf' if style=='snapchat' else 'AlteHaasGroteskBold.ttf')
    def layout(size):
        font = ImageFont.truetype(str(path),size)
        stroke = 0
        lines=[]
        for paragraph in job['title'].splitlines():
            line=''
            for word in paragraph.split():
                candidate=(line+' '+word).strip()
                if font.getlength(candidate)+2*stroke>900 and line:
                    lines.append(line);line=word
                else:line=candidate
            if line:lines.append(line)
        boxes=[font.getbbox(line,stroke_width=stroke) for line in lines]
        height=sum(box[3]-box[1] for box in boxes)+max(0,len(lines)-1)*16
        fits=bool(lines) and all(box[2]-box[0]<=900 for box in boxes)
        return font,stroke,lines,boxes,height,fits
    size=46 if style=='snapchat' else 76
    font,stroke,lines,boxes,height,fits=layout(size)
    if not fits or height>600:
        raise ValueError('Title too long: shorten it; fixed font size is not reduced')
    title=Image.new('RGBA',(1080,1920))
    draw=ImageDraw.Draw(title)
    y=270
    if style=='snapchat':
        draw.rectangle((0,y-36,1079,y+height+36),fill=(70,70,70,170))
    for line,box in zip(lines,boxes):
        left,top,right,bottom=box
        width,h=right-left,bottom-top
        x=(1080-width)//2
        if style=='max_readable':
            draw.rounded_rectangle((x-14,y-9,x+width+14,y+h+9),radius=9,fill='white')
        draw.text((x-left,y-top),line,font=font,fill='white' if style=='snapchat' else 'black')
        y+=h+16
    title.save(work/'title.png')
    save(work/'title-layout.json',dict(style=style,font_size=size,lines=lines,
         ink_height=height,top=270,max_width=900))



def visual_timing(visual, original_duration):
    start,end,speed=visual['start'],visual['end'],visual.get('speed',1)
    if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in (start,end,speed)) or speed < 1 or not 0 <= start < end <= original_duration+.001:
        raise ValueError('Invalid visual range or speed-up; source must contain the full interval.')
    return (end-start)/speed


def voiceover_visual_gate(job):
    if len(job.get('visuals',[])) < 2:
        raise ValueError('Voice-over requires multiple visual clips or snippets.')
    groups={}
    insert_paths={str(media(x['path'])) for x in job.get('voiceover_inserts',[])}
    for visual in job.get('visuals',[]):
        path=media(visual['path'])
        source_duration=duration(path)
        length=visual_timing(visual,source_duration)
        if visual.get('original_audio'):
            if str(path) not in insert_paths:
                raise ValueError('Original-audio visual is not declared in voiceover_inserts.')
            continue
        if source_duration > 5.001:
            if abs(length-1) > .02:
                raise ValueError('Voice-over clips over five seconds require one-second output snippets.')
            groups.setdefault(str(path),[]).append((visual['start'],visual['end']))
    for intervals in groups.values():
        ordered=sorted(intervals)
        if len(ordered) < 2 or any(a[1] > b[0]+.001 for a,b in zip(ordered,ordered[1:])):
            raise ValueError('Each long voice-over clip needs multiple distinct, non-overlapping snippets.')


def video_filter(capture, rotate=0, normalize_mix=.75, look_mix=.30):
    geometry = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30'
    if rotate in (90, -90):
        geometry = ('transpose=clock,' if rotate == 90 else 'transpose=cclock,') + geometry
    if capture in ('phone','graded'):
        return f'[0:v]{geometry}[v]'
    if capture != 'camera':
        raise ValueError('Capture must be phone or camera')
    if not all(isinstance(x,(int,float)) and math.isfinite(x) and 0 <= x <= 1 for x in (normalize_mix,look_mix)):
        raise ValueError('Camera LUT mixes must be between 0 and 1')
    return (f'[0:v]{geometry},format=gbrp,split=2[original][convert];'
            "[convert]lut3d=file=normalize.cube[converted];"
            f"[original][converted]blend=all_expr='A*{1-normalize_mix}+B*{normalize_mix}',split=2[normalized][look];"
            "[look]lut3d=file=look.cube[graded];"
            f"[normalized][graded]blend=all_expr='A*{1-look_mix}+B*{look_mix}',format=yuv420p[v]")


def add_broll(job, work, base, length):
    entries = sorted(job.get('broll', []), key=lambda v: v['at'])
    if not entries:
        return base
    if job['mode'] == 'voiceover':
        raise ValueError('For voice-over put the picture track in visuals, not broll.')
    previous_end = 0
    args = ['-i', base]
    filters = []
    current = '[0:v]'
    for i, entry in enumerate(entries):
        src = media(entry['path'])
        start, end, at = entry['start'], entry['end'], entry['at']
        if not 0 <= start < end <= duration(src)+.01 or at < previous_end or at+end-start > length+.01:
            raise ValueError('Invalid or overlapping B-roll interval')
        if job['broll_mode'] == 'selected' and src not in [media(p) for p in job.get('broll_allowed', [])]:
            raise ValueError('B-roll is not among the selected files')
        if job['broll_mode'] == 'auto' and not entry.get('match'):
            raise ValueError('Automatic B-roll requires a documented content match.')
        name = f'broll{i:04}.mkv'
        ff(['-ss',start,'-i',src,'-t',end-start,'-an','-filter_complex',
            video_filter(entry.get('capture','phone'),entry.get('rotate',0),entry.get('camera_lut_rec709_mix',.75),entry.get('camera_lut_look_mix',.30)),
            '-map','[v]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',name],work)
        args += ['-i', name]
        filters.append(f'[{i+1}:v]setpts=PTS-STARTPTS+{at}/TB[b{i}]')
        filters.append(f"{current}[b{i}]overlay=eof_action=pass:enable='gte(t,{at})*lt(t,{at+end-start})'[o{i}]")
        current = f'[o{i}]'
        previous_end = at+end-start
    ff(args+['-filter_complex',';'.join(filters),'-map',current,'-map','0:a',
             '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','broll-base.mkv'],work)
    return 'broll-base.mkv'


def render(job, work):
    zoom_gate(job)
    title_gate(job)
    cutout_gate(job)
    p = read(work / 'plan.json')
    if not p['reviewed'] or p['job'] != job:
        raise ValueError('Review current plan first; changed job requires replanning')
    events = zoom_timeline(job,p['segments'])
    if events != p.get('zooms',[]):
        raise ValueError('Zoom timeline changed: replan and review')
    for s in p['segments']:
        if not 0 <= s['source'] < len(job['sources']) or not 0 <= s['start'] < s['end']:
            raise ValueError('Invalid edit interval')
    parts = []
    shutil.copy2(TOOLS/'LUTs'/'CINELIKE D to REC 709_26.P1003055.cube', work/'normalize.cube')
    shutil.copy2(TOOLS/'LUTs'/'MERRY_MEN_II.cube', work/'look.cube')
    for n, s in enumerate(p['segments']):
        part = work / f'part{n:04}.mkv'
        args = ['-ss', s['start'], '-i', media(job['sources'][s['source']]), '-t', s['end']-s['start']]
        if job['mode'] == 'voiceover':
            args += ['-vn']
        else:
            capture = job.get('source_captures', [job['capture']]*len(job['sources']))[s['source']]
            args += ['-filter_complex', video_filter(capture,job.get('rotate',0)), '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p']
        ff(args + ['-map', '0:a:0', *([] if job['mode']=='voiceover' else ['-map','[v]']), '-c:a', 'pcm_s16le', '-ar','48000','-ac','2',part],work)
        parts.append(part.name)
    (work / 'concat.txt').write_text(''.join(f"file '{x}'\n" for x in parts), encoding='utf-8')
    ff(['-f','concat','-safe','0','-i','concat.txt','-c','copy','clean.mkv'],work)
    base = 'clean.mkv'
    if job['mode'] == 'voiceover':
        visuals = job.get('visuals', [])
        voiceover_visual_gate(job)
        lengths=[visual_timing(v,duration(media(v['path']))) for v in visuals]
        if sum(lengths) < p['duration']-.02:
            raise ValueError('B-roll does not cover the voice-over')
        visual_parts = []
        for n,v in enumerate(visuals):
            if not 0 <= v['start'] < v['end'] <= duration(media(v['path']))+.02:
                raise ValueError('Invalid B-roll range')
            name = f'visual{n:04}.mkv'
            graph=video_filter(v.get('capture',job['capture']),v.get('rotate',0),v.get('camera_lut_rec709_mix',.75),v.get('camera_lut_look_mix',.30))
            graph+=f";[v]setpts=(PTS-STARTPTS)/{v.get('speed',1)},fps=30[retimed]"
            ff(['-ss',v['start'],'-i',media(v['path']),'-t',v['end']-v['start'],'-an','-filter_complex',graph,'-map','[retimed]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',name],work)
            visual_parts.append(name)
        (work/'visuals.txt').write_text(''.join(f"file '{x}'\n" for x in visual_parts),encoding='utf-8')
        ff(['-f','concat','-safe','0','-i','visuals.txt','-i','clean.mkv','-map','0:v','-map','1:a','-c','copy','-shortest','base.mkv'],work)
        base = 'base.mkv'
    if events:
        ff(['-i',base,'-vf',zoom_filter(events),'-c:v','libx264','-crf','18','-preset','fast',
            '-pix_fmt','yuv420p','-c:a','copy','zoom-base.mkv'],work)
        base = 'zoom-base.mkv'
        zoom_audio(events,work,p['duration'])
    base = add_broll(job,work,base,p['duration'])
    if job.get('title_behind_person'):
        run(['uv','run',Path(__file__).with_name('cutout.py'),work/base,work/'plan.json'])
    # Measure speech once, then apply measured loudness normalization.
    m = {'enabled':False}
    norm = 'anull'
    if job.get('audio_normalize',True):
        measured = ff(['-i',base,'-vn','-af','loudnorm=I=-16:TP=-2:LRA=11:print_format=json','-f','null','-'],work)
        match = re.findall(r'\{\s*"input_i".*?\}',measured,re.S)
        m = json.loads(match[-1])
        if not all(math.isfinite(float(m[k])) for k in ('input_i','input_tp','input_lra','input_thresh','target_offset')):
            raise ValueError('Speech is silent or cannot be normalized')
        norm = f"loudnorm=I=-16:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    ff(['-i',base,'-vn','-af',f'apad=pad_dur=3,{norm},atrim=duration={p["duration"]}', '-c:a','pcm_s16le','-ar','48000','speech-normalized.wav'],work)
    args = ['-i',base,'-i','speech-normalized.wav']
    graph = '[1:a]anull[speech];'
    mix = '[speech]'
    count = 1
    if job.get('music'):
        music_start = float(job.get('music_start',30))
        if not 0 <= music_start < duration(media(job['music'])):
            raise ValueError('Music start must be within the selected track; set music_start for short tracks.')
        args += ['-stream_loop','-1','-ss',music_start,'-i',media(job['music'])]
        graph += f"[2:a]volume={float(job.get('music_db',-20))}dB[music];"
        mix += '[music]'
        count += 1
    if events:
        args += ['-i','zoom-sfx.wav']
        mix += f'[{3 if job.get("music") else 2}:a]'
        count += 1
    graph += mix+(f'amix=inputs={count}:duration=first:normalize=0,' if count>1 else '')+'alimiter=limit=0.794:level=false:latency=true[a]'
    args += ['-filter_complex',graph,'-map','0:v:0','-map','[a]']
    if job.get('captions') or job.get('title'):
        captions({'title_duration':p['duration'], **job},p['words'],work)
        fontdir = work / 'fonts'
        fontdir.mkdir(exist_ok=True)
        for f in (TOOLS/'fonts').glob('*'):
            if f.suffix.lower() in ('.ttf','.otf'):
                shutil.copy2(f,fontdir/f.name)
        args += ['-vf',visual_filter(job,p)]
    log = ff(args+['-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-t',p['duration'],'final.mp4'],work)
    (work/'render.log').write_text(log,encoding='utf-8')
    ff(['-v','error','-i','final.mp4','-f','null','-'],work)
    actual = duration(work/'final.mp4')
    if abs(actual-p['duration']) > max(.25,len(parts)/30):
        raise ValueError('Final duration differs from plan')
    peaks = ff(['-i','final.mp4','-vn','-af','ebur128=peak=true','-f','null','-'],work)
    peak = re.findall(r'Peak:\s+(-?[\d.]+) dBFS',peaks)
    if not peak or float(peak[-1]) > -1:
        raise ValueError('Final true peak exceeds -1 dBFS or could not be measured')
    save(work/'render-check.json',{'duration':actual,'expected':p['duration'],'true_peak_dbfs':float(peak[-1]),'sha256':digest(work/'final.mp4'),'plan_sha256':digest(work/'plan.json'),'speech_measurement':m})


def finish(job, work):
    if job.get('qa_approved') is not True:
        raise ValueError('Review the actual render before archiving')
    check = read(work/'render-check.json')
    planned_job = read(work/'plan.json')['job']
    if {k:v for k,v in job.items() if k != 'qa_approved'} != {k:v for k,v in planned_job.items() if k != 'qa_approved'}:
        raise ValueError('Job changed after render')
    if check['sha256'] != digest(work/'final.mp4') or check['plan_sha256'] != digest(work/'plan.json'):
        raise ValueError('Render or plan changed after checks')
    dest = PROJECTS/'finished_projects'/job['project']
    dest.mkdir(parents=True,exist_ok=False)
    originals = dest/'originals'
    originals.mkdir()
    paths = list(dict.fromkeys(job['sources']+job.get('archive_sources',[])+[v['path'] for v in job.get('visuals',[])+job.get('broll',[])]))
    manifest=[]
    for i,path in enumerate(paths):
        src=media(path)
        target=originals/f'{i:03}_{src.name}'
        shutil.copy2(src,target)
        if digest(src)!=digest(target):
            raise ValueError('Original copy checksum mismatch')
        manifest.append({'source':str(src),'copy':str(target.relative_to(dest)),'sha256':digest(target)})
    for name in ('final.mp4','plan.json','render-check.json'):
        shutil.copy2(work/name,dest/name)
    save(dest/'originals.json',manifest)
    # Remove only the verified selected input copies inside the input area.
    # External sources and shared B-roll libraries are always retained.
    input_root = (PROJECTS/'unfinished_projects').resolve()
    for entry in manifest:
        src = Path(entry['source']).resolve()
        archived = dest/entry['copy']
        if src.is_relative_to(input_root) and digest(src) == entry['sha256'] == digest(archived):
            src.unlink()
    print(dest)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','plan','render','finish'])
    parser.add_argument('job',type=Path)
    args=parser.parse_args()
    job=read(args.job)
    gate(job)
    globals()[args.command](job,args.job.resolve().parent)
