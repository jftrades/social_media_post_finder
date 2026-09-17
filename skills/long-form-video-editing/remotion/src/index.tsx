import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Composition,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  registerRoot,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

type OverlayKind = 'default' | 'note' | 'race';

type Overlay = {
  startFrame: number;
  durationFrames: number;
  text: string;
  kind?: OverlayKind;
  x?: number;
  y?: number;
  fontSize?: number;
  rotation?: number;
};

type Zoom = {
  startFrame: number;
  endFrame: number;
  scale: number;
  x?: number;
  y?: number;
};

type TimedAudio = {
  startFrame: number;
  endFrame?: number;
  src: string;
  volume?: number;
  fadeInFrames?: number;
  fadeOutFrames?: number;
};

type CounterOverlay = {
  startFrame: number;
  durationFrames: number;
  label: string;
  target?: string | number;
  repFrames: number[];
  suffix?: string;
};

type ImageOverlay = {
  startFrame: number;
  durationFrames: number;
  src: string;
  mode?: 'full' | 'card';
  x?: number;
  y?: number;
  width?: number;
};

type VideoOverlay = {
  startFrame: number;
  durationFrames: number;
  src: string;
  sourceStartFrame?: number;
  fit?: 'cover' | 'contain';
};

export type LongFormProps = {
  baseVideo: string;
  durationInFrames: number;
  fps: number;
  width: number;
  height: number;
  overlays: Overlay[];
  zooms: Zoom[];
  soundEffects: TimedAudio[];
  music: TimedAudio[];
  counters: CounterOverlay[];
  imageOverlays: ImageOverlay[];
  videoOverlays: VideoOverlay[];
  thumbnailSource: string;
  thumbnailTitle: string;
  thumbnailAccent?: string;
};

const defaults: LongFormProps = {
  baseVideo: 'runtime/media/base.mp4',
  durationInFrames: 150,
  fps: 30,
  width: 1920,
  height: 1080,
  overlays: [],
  zooms: [],
  soundEffects: [],
  music: [],
  counters: [],
  imageOverlays: [],
  videoOverlays: [],
  thumbnailSource: 'runtime/media/thumbnail-source.jpg',
  thumbnailTitle: 'LONG FORM',
  thumbnailAccent: 'VIDEO',
};

const fonts = `
@font-face {font-family: 'Alte Haas'; src: url('${staticFile('runtime/fonts/AlteHaasGroteskBold.ttf')}'); font-weight: 700;}
@font-face {font-family: 'Child Hood'; src: url('${staticFile('runtime/fonts/Child Hood.otf')}');}
@font-face {font-family: 'Race Day'; src: url('${staticFile('runtime/fonts/Raceday.otf')}');}
`;

const AudioLayer: React.FC<{item: TimedAudio; index: number}> = ({item, index}) => {
  const duration = item.endFrame === undefined ? undefined : Math.max(1, item.endFrame - item.startFrame);
  const baseVolume = item.volume ?? 1;
  return (
    <Sequence key={`${item.src}-${index}`} from={item.startFrame} durationInFrames={duration}>
      <Audio
        src={staticFile(item.src)}
        volume={(relativeFrame) => {
          if (duration === undefined) return baseVolume;
          const fadeIn = Math.max(0, item.fadeInFrames ?? 0);
          const fadeOut = Math.max(0, item.fadeOutFrames ?? 0);
          const inGain = fadeIn === 0 ? 1 : interpolate(relativeFrame, [0, fadeIn], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          const outGain = fadeOut === 0 ? 1 : interpolate(relativeFrame, [duration - fadeOut, duration], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return baseVolume * Math.min(inGain, outGain);
        }}
      />
    </Sequence>
  );
};

const TextOverlay: React.FC<{item: Overlay}> = ({item}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const intro = spring({frame, fps, config: {damping: 14, stiffness: 180, mass: 0.7}});
  const outroStart = Math.max(0, item.durationFrames - Math.round(fps * 0.22));
  const opacity = interpolate(frame, [outroStart, item.durationFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const kind = item.kind ?? 'default';
  const family = kind === 'note' ? 'Child Hood' : kind === 'race' ? 'Race Day' : 'Alte Haas';
  const color = kind === 'note' ? '#fff5c2' : '#ffffff';
  return (
    <div
      style={{
        position: 'absolute',
        left: item.x ?? 960,
        top: item.y ?? 540,
        transform: `translate(-50%, -50%) rotate(${item.rotation ?? 0}deg) scale(${0.78 + intro * 0.22})`,
        opacity,
        maxWidth: 1500,
        textAlign: 'center',
        color,
        fontFamily: family,
        fontSize: item.fontSize ?? (kind === 'race' ? 126 : kind === 'note' ? 82 : 96),
        lineHeight: 0.96,
        letterSpacing: kind === 'default' ? -2 : 0,
        textShadow: '0 8px 22px rgba(0,0,0,0.72), 0 2px 5px rgba(0,0,0,0.9)',
        whiteSpace: 'pre-line',
      }}
    >
      {item.text}
    </div>
  );
};

const Counter: React.FC<{item: CounterOverlay}> = ({item}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const count = item.repFrames.filter((value) => value <= frame).length;
  const last = [...item.repFrames].reverse().find((value) => value <= frame) ?? -1000;
  const bump = spring({frame: frame - last, fps, config: {damping: 10, stiffness: 220, mass: 0.45}});
  return (
    <div style={{position: 'absolute', left: 42, top: 38, minWidth: 285, padding: '17px 22px 15px', borderRadius: 18, background: 'rgba(8,8,8,.76)', border: '1px solid rgba(255,255,255,.18)', boxShadow: '0 10px 30px rgba(0,0,0,.35)', color: 'white', fontFamily: 'Alte Haas', textShadow: '0 5px 15px rgba(0,0,0,.75)'}}>
      <div style={{fontSize: 29, letterSpacing: -0.6}}>{item.label}{item.target === undefined ? '' : ` · Ziel: ${item.target}`}</div>
      <div style={{fontSize: 66, lineHeight: 0.95, marginTop: 8, transform: `scale(${1 + bump * 0.08})`, transformOrigin: 'left center'}}>{count}{item.suffix ?? ''}</div>
    </div>
  );
};

const Picture: React.FC<{item: ImageOverlay}> = ({item}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const intro = spring({frame, fps, config: {damping: 15, stiffness: 160, mass: 0.65}});
  if ((item.mode ?? 'full') === 'full') {
    return (
      <AbsoluteFill style={{backgroundColor: '#080808', opacity: intro}}>
        <Img src={staticFile(item.src)} style={{position: 'absolute', inset: -30, width: 'calc(100% + 60px)', height: 'calc(100% + 60px)', objectFit: 'cover', filter: 'blur(28px) brightness(.28)', transform: 'scale(1.08)'}} />
        <Img src={staticFile(item.src)} style={{width: '100%', height: '100%', objectFit: 'contain', filter: 'drop-shadow(0 14px 32px rgba(0,0,0,.65))', transform: `scale(${0.96 + intro * 0.04})`}} />
      </AbsoluteFill>
    );
  }
  return <Img src={staticFile(item.src)} style={{position: 'absolute', left: item.x ?? 1220, top: item.y ?? 90, width: item.width ?? 620, maxHeight: 850, objectFit: 'contain', borderRadius: 22, boxShadow: '0 16px 46px rgba(0,0,0,.55)', transform: `scale(${0.9 + intro * 0.1})`, transformOrigin: 'top left'}} />;
};

const LongFormVideo: React.FC<{props: LongFormProps; withMusic: boolean}> = ({props, withMusic}) => {
  const frame = useCurrentFrame();
  const activeZoom = props.zooms.find((zoom) => frame >= zoom.startFrame && frame <= zoom.endFrame);
  let scale = 1;
  let translateX = 0;
  let translateY = 0;
  if (activeZoom) {
    const edge = Math.max(2, Math.min(10, Math.round((activeZoom.endFrame - activeZoom.startFrame) / 3)));
    const eased = interpolate(
      frame,
      [activeZoom.startFrame, activeZoom.startFrame + edge, activeZoom.endFrame - edge, activeZoom.endFrame],
      [1, activeZoom.scale, activeZoom.scale, 1],
      {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
    );
    scale = eased;
    translateX = (activeZoom.x ?? 0) * (eased - 1);
    translateY = (activeZoom.y ?? 0) * (eased - 1);
  }
  return (
    <AbsoluteFill style={{backgroundColor: '#000', overflow: 'hidden'}}>
      <style>{fonts}</style>
      <AbsoluteFill style={{transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`}}>
        <OffthreadVideo src={staticFile(props.baseVideo)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      {props.videoOverlays.map((item, index) => (
        <Sequence key={`video-${item.src}-${index}`} from={item.startFrame} durationInFrames={item.durationFrames}>
          <OffthreadVideo muted startFrom={item.sourceStartFrame ?? 0} src={staticFile(item.src)} style={{width: '100%', height: '100%', objectFit: item.fit ?? 'cover'}} />
        </Sequence>
      ))}
      {props.overlays.map((item, index) => (
        <Sequence key={`${item.text}-${index}`} from={item.startFrame} durationInFrames={item.durationFrames}>
          <TextOverlay item={item} />
        </Sequence>
      ))}
      {props.counters.map((item, index) => (
        <Sequence key={`counter-${item.label}-${index}`} from={item.startFrame} durationInFrames={item.durationFrames}>
          <Counter item={item} />
        </Sequence>
      ))}
      {props.imageOverlays.map((item, index) => (
        <Sequence key={`image-${item.src}-${index}`} from={item.startFrame} durationInFrames={item.durationFrames}>
          <Picture item={item} />
        </Sequence>
      ))}
      {props.soundEffects.map((item, index) => <AudioLayer key={`sfx-${index}`} item={item} index={index} />)}
      {withMusic && props.music.map((item, index) => <AudioLayer key={`music-${index}`} item={item} index={index} />)}
    </AbsoluteFill>
  );
};

const Thumbnail: React.FC<LongFormProps> = (props) => (
  <AbsoluteFill style={{backgroundColor: '#080808'}}>
    <style>{fonts}</style>
    <Img src={staticFile(props.thumbnailSource)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(0,0,0,.84) 0%, rgba(0,0,0,.35) 58%, rgba(0,0,0,.08) 100%)'}} />
    <div style={{position: 'absolute', left: 78, top: 370, width: 980, color: 'white', fontFamily: 'Alte Haas', fontSize: 112, lineHeight: 0.88, letterSpacing: -4, textShadow: '0 8px 24px rgba(0,0,0,.8)', whiteSpace: 'pre-line'}}>
      {props.thumbnailTitle}
    </div>
    {props.thumbnailAccent ? <div style={{position: 'absolute', left: 86, top: 610, color: '#ffdf35', fontFamily: 'Race Day', fontSize: 82, transform: 'rotate(-2deg)', textShadow: '0 7px 18px rgba(0,0,0,.8)'}}>{props.thumbnailAccent}</div> : null}
  </AbsoluteFill>
);

const Root: React.FC = () => (
  <>
    <Composition
      id="LongFormAnimated"
      component={(props: LongFormProps) => <LongFormVideo props={props} withMusic={false} />}
      defaultProps={defaults}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={150}
      calculateMetadata={({props}) => ({durationInFrames: props.durationInFrames, fps: props.fps, width: props.width, height: props.height})}
    />
    <Composition
      id="LongFormFinal"
      component={(props: LongFormProps) => <LongFormVideo props={props} withMusic />}
      defaultProps={defaults}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={150}
      calculateMetadata={({props}) => ({durationInFrames: props.durationInFrames, fps: props.fps, width: props.width, height: props.height})}
    />
    <Composition id="Thumbnail" component={Thumbnail} defaultProps={defaults} width={1280} height={720} fps={1} durationInFrames={1} />
  </>
);

registerRoot(Root);
