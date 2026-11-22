// One Day, One Image — Saturday 21 November 2026.
//
// Entry program for make.fun's news-image-20261121. The picture itself is
// entry.png in this repository (1024x1024, drawn from scratch by
// generate.py from reporting published on 21 November 2026: 51 sourced
// stories across 7 regions, a UTC timeline and an explicit date check).
// This program only places that exact file at /output/entry.png for the
// grader.
//
// Node 22, standard library only, no network, fully deterministic: every
// run writes the same bytes, so the grader's two runs agree.
//
// Try it locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The output folder is created when missing and never removed. Deleting it
// would fail in the grader sandbox, whose parent directory is read-only,
// so this program only ever writes one file inside it.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1048576;
const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

const here = fileURLToPath(new URL(".", import.meta.url));
const input = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const output = join(outDir, "entry.png");

const bytes = readFileSync(input);
if (bytes.length < PNG_MAGIC.length || bytes.length > MAX_BYTES) {
  throw new Error(
    `entry.png is ${bytes.length} bytes, outside 8..${MAX_BYTES}`,
  );
}
if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  throw new Error("entry.png does not begin with the PNG magic bytes");
}

if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}
writeFileSync(output, bytes);

const back = readFileSync(output);
if (back.length !== bytes.length || !back.equals(bytes)) {
  throw new Error("the file written to the output directory differs from entry.png");
}
console.log(`entry.png -> ${output} (${bytes.length} bytes)`);
