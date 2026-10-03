import { test } from "node:test";
import assert from "node:assert/strict";
import { shorten } from "./shorten.js";

test("shortens ids", () => {
  assert.equal(shorten(0), "a");
  assert.equal(shorten(36), "ba");
});
