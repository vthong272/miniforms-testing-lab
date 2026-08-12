import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

test("navigation labels cannot capture drag-selection gestures", async () => {
  const css = await readFile(new URL("../../app/css/style.css", import.meta.url), "utf8");

  assert.match(css, /\.nav-item\s*\{[^}]*user-select:\s*none;/s);
  assert.match(css, /\.nav-item\s*>\s*\*\s*\{[^}]*pointer-events:\s*none;/s);
});

test("deployment HTML contains all three complete form panels", async () => {
  const html = await readFile(new URL("../../app/index.html", import.meta.url), "utf8");

  for (const panel of ["registration", "shipping", "loan"]) {
    assert.match(html, new RegExp(`<section id="${panel}"`));
    assert.match(html, new RegExp(`<form id="${panel}-form"`));
  }
  assert.doesNotMatch(html, /tokens truncated|…\d+ tokens/);
});
