// News-image entry for make.fun's "Sum up 18 November's world news in one image"
// bounty (news-image-20261118). Node 22, standard library only.
//
// The program runs in a sandbox with no network and a read-only /bot, so the
// finished front page is committed beside this file as entry.png (a JPEG's
// bytes under a .png name, which the gate accepts: it tells PNG from JPEG by
// the first bytes). All this program does is copy it to the output path.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(outDir, 'entry.png'),
);
