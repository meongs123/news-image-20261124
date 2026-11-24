// news-image-20261124 — Tuesday 24 November 2026 front page (Node 22,
// standard library only). The image is entry.png beside this file, drawn
// in code by compose.py; this program copies it to /output/entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const dest = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');

copyFileSync(src, dest);

// Guards: refuse to hand the grader a file that cannot pass its gate.
const bytes = readFileSync(dest);
const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngSig)) {
  throw new Error('entry.png is not a PNG');
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, not 1024x1024`);
}
// Round-trip check: what was copied must be byte-identical to the source.
const original = readFileSync(src);
if (!bytes.equals(original)) {
  throw new Error('copied entry.png differs from the repository copy');
}
console.log(`wrote ${dest} (${statSync(dest).size} bytes, 1024x1024)`);
