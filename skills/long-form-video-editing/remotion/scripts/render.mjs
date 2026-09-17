import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';

const args = process.argv.slice(2);
const get = (name) => {
  const index = args.indexOf(name);
  if (index === -1 || index === args.length - 1) throw new Error(`Missing ${name}`);
  return args[index + 1];
};

const propsPath = path.resolve(get('--props'));
const outputDir = path.resolve(get('--output-dir'));
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const inputProps = JSON.parse(fs.readFileSync(propsPath, 'utf8'));
fs.mkdirSync(outputDir, {recursive: true});

const serveUrl = await bundle({
  entryPoint: path.join(root, 'src', 'index.tsx'),
  publicDir: path.join(root, 'public'),
  webpackOverride: (config) => config,
});

for (const [id, filename] of [['LongFormAnimated', '02_animated.mp4'], ['LongFormFinal', '03_final.mp4']]) {
  const composition = await selectComposition({serveUrl, id, inputProps});
  await renderMedia({
    composition,
    serveUrl,
    codec: 'h264',
    audioCodec: 'aac',
    audioBitrate: '256K',
    crf: 18,
    pixelFormat: 'yuv420p',
    outputLocation: path.join(outputDir, filename),
    inputProps,
    overwrite: true,
    concurrency: '25%',
  });
}

const thumbnail = await selectComposition({serveUrl, id: 'Thumbnail', inputProps});
await renderStill({
  composition: thumbnail,
  serveUrl,
  output: path.join(outputDir, 'thumbnail.jpg'),
  inputProps,
  imageFormat: 'jpeg',
  jpegQuality: 95,
  overwrite: true,
});
