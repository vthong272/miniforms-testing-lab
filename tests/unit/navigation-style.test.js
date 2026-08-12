import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("navigation labels cannot capture drag-selection gestures", async () => {
  const css = await readFile(new URL("../../app/css/style.css", import.meta.url), "utf8");

  assert.match(css, /\.nav-item\s*\{[^}]*user-select:\s*none;/s);
  assert.match(css, /\.nav-item\s*>\s*\*\s*\{[^}]*pointer-events:\s*none;/s);
});
