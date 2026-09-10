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
    if job.get('intake_confirmed') is not True or not all(job.get('intake', {}).get(k) for k in ('cleanup', 'clips', 'captions', 'music', 'title', 'broll', 'capture')):
        raise ValueError('First ask and receive all seven intake answers. No editing before intake.')
    if job.get('capture') not in ('phone', 'camera'):
        raise ValueError('Choose phone or camera capture.')
    if job.get('broll_mode') not in ('none', 'specific', 'selected', 'auto'):
        raise ValueError('Choose a B-roll mode.')
    if job.get('broll_mode') == 'none' and job.get('broll'):
        raise ValueError('B-roll is disabled.')
    if 'title' not in job or not isinstance(job['title'], str):
        raise ValueError('Set title text, or an empty string for no title.')
    if not re.fullmatch(r'[\w-]+', job['project']):
        raise ValueError('Project name must contain only letters, numbers, hyphens or underscores.')
    if job['mode'] not in ('single', 'multi', 'voiceover'):
        raise ValueError('Invalid mode')
    if not job['sources'] or (job['mode'] == 'single' and len(job['sources']) != 1):
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
        for start, end in intervals:
            segments.append({'source': i, 'start': start, 'end': end})
            for w in kept:
                if start <= w['start'] and w['end'] <= end:
                    output_words.append({'word': w['word'], 'start': offset+w['start']-start, 'end': offset+w['end']-start})
            offset += end-start
    if not segments:
        raise ValueError('Empty edit')
    save(work / 'plan.json', {'reviewed': False, 'job': job, 'segments': segments, 'words': output_words, 'duration': offset})


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
        from PIL import Image, ImageDraw, ImageFont
        font = ImageFont.truetype(str(TOOLS/'fonts'/'AlteHaasGroteskBold.ttf'), 76)
        lines = []
        for paragraph in job['title'].splitlines():
            line = ''
            for word in paragraph.split():
                candidate = (line + ' ' + word).strip()
                if font.getlength(candidate) > 900 and line:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            if line:
                lines.append(line)
        if not lines or len(lines) > 3 or any(font.getlength(line) > 900 for line in lines):
            raise ValueError('Title too long: shorten it or split long words.')
        # Draw text and its tight per-line background with the same font metrics.
        title = Image.new('RGBA', (1080, 1920))
        draw = ImageDraw.Draw(title)
        y = 240
        for line in lines:
            left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
            width, height = right-left, bottom-top
            x = (1080-width)//2
            draw.rounded_rectangle((x-14, y-9, x+width+14, y+height+9),
                                   radius=9, fill='white')
            draw.text((x-left, y-top), line, font=font, fill='black')
            y += height+16
        title.save(work/'title.png')
    (work / 'captions.ass').write_text(header, encoding='utf-8')


def video_filter(capture, rotate=0):
    geometry = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30'
    if rotate in (90, -90):
        geometry = ('transpose=clock,' if rotate == 90 else 'transpose=cclock,') + geometry
    if capture == 'phone':
        return f'[0:v]{geometry}[v]'
    if capture != 'camera':
        raise ValueError('Capture must be phone or camera')
    return (f'[0:v]{geometry},format=gbrp,split=2[original][convert];'
            "[convert]lut3d=file=normalize.cube[converted];"
            "[original][converted]blend=all_expr='A*0.25+B*0.75',split=2[normalized][look];"
            "[look]lut3d=file=look.cube[graded];"
            "[normalized][graded]blend=all_expr='A*0.70+B*0.30',format=yuv420p[v]")


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
            video_filter(entry.get('capture','phone'),entry.get('rotate',0)),
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
    p = read(work / 'plan.json')
    if not p['reviewed'] or p['job'] != job:
        raise ValueError('Review current plan first; changed job requires replanning')
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
        if sum(v['end']-v['start'] for v in visuals) < p['duration']-.02:
            raise ValueError('B-roll does not cover the voice-over')
        visual_parts = []
        for n,v in enumerate(visuals):
            if not 0 <= v['start'] < v['end'] <= duration(media(v['path']))+.02:
                raise ValueError('Invalid B-roll range')
            name = f'visual{n:04}.mkv'
            ff(['-ss',v['start'],'-i',media(v['path']),'-t',v['end']-v['start'],'-an','-filter_complex',video_filter(v.get('capture','phone'),v.get('rotate',0)),'-map','[v]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',name],work)
            visual_parts.append(name)
        (work/'visuals.txt').write_text(''.join(f"file '{x}'\n" for x in visual_parts),encoding='utf-8')
        ff(['-f','concat','-safe','0','-i','visuals.txt','-i','clean.mkv','-map','0:v','-map','1:a','-c','copy','-shortest','base.mkv'],work)
        base = 'base.mkv'
    base = add_broll(job,work,base,p['duration'])
    # Measure speech once, then apply measured loudness normalization.
    measured = ff(['-i',base,'-vn','-af','loudnorm=I=-16:TP=-2:LRA=11:print_format=json','-f','null','-'],work)
    match = re.findall(r'\{\s*"input_i".*?\}',measured,re.S)
    m = json.loads(match[-1])
    if not all(math.isfinite(float(m[k])) for k in ('input_i','input_tp','input_lra','input_thresh','target_offset')):
        raise ValueError('Speech is silent or cannot be normalized')
    norm = f"loudnorm=I=-16:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    ff(['-i',base,'-vn','-af',f'apad=pad_dur=3,{norm},atrim=duration={p["duration"]}', '-c:a','pcm_s16le','-ar','48000','speech-normalized.wav'],work)
    args = ['-i',base,'-i','speech-normalized.wav']
    graph = '[1:a]anull[speech];'
    if job.get('music'):
        music_start = float(job.get('music_start',30))
        if not 0 <= music_start < duration(media(job['music'])):
            raise ValueError('Music start must be within the selected track; set music_start for short tracks.')
        args += ['-stream_loop','-1','-ss',music_start,'-i',media(job['music'])]
        graph += f"[2:a]volume={float(job.get('music_db',-20))}dB[music];[speech][music]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.794:level=false:latency=true[a]"
    else:
        graph += '[speech]alimiter=limit=0.794:level=false:latency=true[a]'
    args += ['-filter_complex',graph,'-map','0:v:0','-map','[a]']
    if job.get('captions') or job.get('title'):
        captions({'title_duration':p['duration'], **job},p['words'],work)
        fontdir = work / 'fonts'
        fontdir.mkdir(exist_ok=True)
        for f in (TOOLS/'fonts').glob('*'):
            if f.suffix.lower() in ('.ttf','.otf'):
                shutil.copy2(f,fontdir/f.name)
        visual = 'ass=captions.ass:fontsdir=fonts'
        if job.get('title'):
            title_end = float(job.get('title_duration', p['duration']))
            if not math.isfinite(title_end) or title_end <= 0:
                raise ValueError('Title duration must be positive and finite')
            visual += f"[sub];movie=title.png[title];[sub][title]overlay=eof_action=repeat:enable='lt(t,{title_end})'"
        args += ['-vf',visual]
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
    paths = list(dict.fromkeys(job['sources']+[v['path'] for v in job.get('visuals',[])+job.get('broll',[])]))
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
