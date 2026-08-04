const test = require("node:test");
const assert = require("node:assert/strict");
const { ValidationError, normalizeItem, buildQueue, recordOutcome, summarizeHistory } = require("../app/inventory.js");

const item = (overrides = {}) => ({ id: "food-1", name: "Greek yogurt", category: "dairy", quantity: 2, unit: "cups", value: 4500, expiresOn: "2026-08-05", addedOn: "2026-08-01", ...overrides });

test("normalizes item text and numeric fields", () => {
  const result = normalizeItem(item({ name: "  Greek   yogurt ", quantity: "2", value: "4500" }));
  assert.equal(result.name, "Greek yogurt");
  assert.equal(result.quantity, 2);
  assert.equal(result.value, 4500);
});

test("rejects unknown category and invalid quantity", () => {
  assert.throws(() => normalizeItem(item({ category: "unknown" })), ValidationError);
  assert.throws(() => normalizeItem(item({ quantity: 0 })), ValidationError);
});

test("rejects malformed expiry date", () => {
  assert.throws(() => normalizeItem(item({ expiresOn: "tomorrow" })), ValidationError);
});

test("orders expired, today, soon, and later items", () => {
  const queue = buildQueue([
    item({ id: "later", expiresOn: "2026-08-12" }),
    item({ id: "today", expiresOn: "2026-08-04" }),
    item({ id: "expired", expiresOn: "2026-08-03" }),
    item({ id: "soon", expiresOn: "2026-08-06" }),
  ], "2026-08-04");
  assert.deepEqual(queue.items.map(entry => entry.id), ["expired", "today", "soon", "later"]);
});

test("calculates urgent count and value at risk", () => {
  const result = buildQueue([item(), item({ id: "food-2", value: 7000, expiresOn: "2026-08-10" })], "2026-08-04");
  assert.equal(result.summary.urgentItems, 1);
  assert.equal(result.summary.valueAtRisk, 4500);
});

test("records consumption and removes the selected item", () => {
  const result = recordOutcome([item()], [], "food-1", "consumed", "2026-08-04");
  assert.equal(result.items.length, 0);
  assert.equal(result.history[0].outcome, "consumed");
});

test("rejects unknown item outcome", () => {
  assert.throws(() => recordOutcome([item()], [], "food-1", "donated", "2026-08-04"), ValidationError);
});

test("summarizes saved and wasted value separately", () => {
  const summary = summarizeHistory([{ outcome: "consumed", value: 4500 }, { outcome: "wasted", value: 2000 }]);
  assert.deepEqual(summary, { savedValue: 4500, wastedValue: 2000, actions: 2 });
});
