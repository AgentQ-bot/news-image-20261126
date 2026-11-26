// Entry point for the 26 November 2026 news-image entry.
// Copies the poster shipped in this repository to the output folder
// the grader reads, creating that folder first when it is missing.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`poster not found beside main.ts: ${source}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`poster written to ${target}`);
