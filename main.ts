// Meme Sprint 3: AI Agent Goes Rogue — entrypoint.
// Copies the verified meme image into the grader's output directory.
// Output is exactly the verified 1024x1024 entry.png, byte for byte.
import { cpSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";

const root = fileURLToPath(new URL(".", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
cpSync(join(root, "entry.png"), join(outDir, "entry.png"));
