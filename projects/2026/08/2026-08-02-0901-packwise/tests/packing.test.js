import test from "node:test";
import assert from "node:assert/strict";
import { calculateSummary, normalizeItem, parsePlan, serializePlan, validateAllowance } from "../app/packing.js";

const items = [
  { id: "a", name: "Shirt", category: "clothes", quantity: 3, unitGrams: 200, packed: true },
  { id: "b", name: "Camera", category: "electronics", quantity: 1, unitGrams: 900, packed: false },
];

test("calculates total, remaining weight, and packing progress", () => {
  const result = calculateSummary(items, 5);
  assert.equal(result.totalGrams, 1500);
  assert.equal(result.remainingGrams, 3500);
  assert.equal(result.packedUnits, 3);
  assert.equal(result.progressPct, 75);
  assert.equal(result.status, "safe");
});

test("marks a plan over the allowance", () => {
  const result = calculateSummary(items, 1);
  assert.equal(result.status, "over");
  assert.equal(result.remainingGrams, -500);
});

test("marks load at 85 percent as near", () => {
  const result = calculateSummary([{...items[1], unitGrams: 850}], 1);
  assert.equal(result.status, "near");
});

test("rejects invalid allowance and item fields", () => {
  assert.throws(() => validateAllowance(0), /between/);
  assert.throws(() => normalizeItem({...items[0], quantity: 1.5}), /integer/);
  assert.throws(() => normalizeItem({...items[0], category: "unknown"}), /category/);
});

test("normalizes whitespace and boolean packing state", () => {
  const item = normalizeItem({...items[0], name: "  Shirt  ", packed: 1});
  assert.equal(item.name, "Shirt");
  assert.equal(item.packed, true);
});

test("round-trips a versioned plan backup", () => {
  const plan = { tripName: "Weekend", allowanceKg: 7, items };
  assert.deepEqual(parsePlan(serializePlan(plan)), plan);
  assert.throws(() => parsePlan('{"version":2,"items":[]}'), /Unsupported/);
});
