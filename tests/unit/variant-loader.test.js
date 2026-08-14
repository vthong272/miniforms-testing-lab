import test from "node:test";
import assert from "node:assert/strict";

import { resolveVariant, targetForVariant } from "../../app/js/variant-loader.js";

test("variant resolver permits only golden and registered mutant IDs", () => {
  assert.equal(resolveVariant(null), "golden");
  assert.equal(resolveVariant("M01"), "M01");
  assert.equal(resolveVariant("M18"), "M18");
  assert.equal(resolveVariant("M19"), "golden");
  assert.equal(resolveVariant("../../secret"), "golden");
});

test("variant target mapping identifies the single mutated form", () => {
  assert.equal(targetForVariant("M01"), "registration");
  assert.equal(targetForVariant("M09"), "shipping");
  assert.equal(targetForVariant("M18"), "loan");
  assert.equal(targetForVariant("golden"), null);
});
