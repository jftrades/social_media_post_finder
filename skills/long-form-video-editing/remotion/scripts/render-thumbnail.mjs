import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';

const args = process.argv.slice(2);
const get = (name) => {
  const index = args.indexOf(name);
  if (index === -1 || index === args.length - 1) throw new Error(`Missing ${name}`);
  return args[index + 1];
};

const propsPath = path.resolve(get('--props'));
const output = path.resolve(get('--output'));
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const inputProps = JSON.parse(fs.readFileSync(propsPath, 'utf8'));
const serveUrl = await bundle({
  entryPoint: path.join(root, 'src', 'index.tsx'),
  publicDir: path.join(root, 'public'),
  webpackOverride: (config) => config,
});
const thumbnail = await selectComposition({serveUrl, id: 'Thumbnail', inputProps});
await renderStill({
  composition: thumbnail,
  serveUrl,
  output,
  inputProps,
  imageFormat: 'jpeg',
  jpegQuality: 95,
  overwrite: true,
});
