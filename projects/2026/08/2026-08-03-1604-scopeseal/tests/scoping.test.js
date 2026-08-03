const test = require("node:test");
const assert = require("node:assert/strict");
const { ValidationError, normalizeContract, normalizeRequest, evaluateRequests, updateStatus } = require("../app/scoping.js");

const contract = (overrides = {}) => ({ projectName: "Brand Site", clientAlias: "B Studio", includedRounds: 2, hourlyRate: 60000, ...overrides });
const request = (overrides = {}) => ({ id: "req-1", title: "Hero image", detail: "Replace image", inScope: true, estimatedHours: 2, status: "new", createdOn: "2026-08-03", ...overrides });

test("normalizes contract text and numeric values", () => {
  const result = normalizeContract(contract({ projectName: "  Brand   Site ", includedRounds: "2", hourlyRate: "60000" }));
  assert.equal(result.projectName, "Brand Site");
  assert.equal(result.includedRounds, 2);
  assert.equal(result.hourlyRate, 60000);
});

test("rejects invalid contract limits", () => {
  assert.throws(() => normalizeContract(contract({ includedRounds: 21 })), ValidationError);
  assert.throws(() => normalizeContract(contract({ hourlyRate: 9000 })), ValidationError);
});

test("normalizes request and boolean scope flag", () => {
  const result = normalizeRequest(request({ inScope: "true", estimatedHours: "2.5" }));
  assert.equal(result.inScope, true);
  assert.equal(result.estimatedHours, 2.5);
});

test("rejects invalid half-hour increments", () => {
  assert.throws(() => normalizeRequest(request({ estimatedHours: 1.2 })), ValidationError);
});

test("uses included allowances in request order", () => {
  const result = evaluateRequests(contract(), [request({ id: "a" }), request({ id: "b" })]);
  assert.equal(result.requests[0].billable, false);
  assert.equal(result.requests[1].billable, false);
  assert.equal(result.summary.remainingRounds, 0);
});

test("charges in-scope work after allowance is exhausted", () => {
  const result = evaluateRequests(contract({ includedRounds: 1 }), [request({ id: "a" }), request({ id: "b", estimatedHours: 1.5 })]);
  assert.equal(result.requests[1].reason, "포함 횟수 초과");
  assert.equal(result.requests[1].charge, 90000);
});

test("charges out-of-scope work and summarizes exposure", () => {
  const result = evaluateRequests(contract(), [request({ id: "a", inScope: false, estimatedHours: 6, status: "quoted" }), request({ id: "b", inScope: false, estimatedHours: 2 })]);
  assert.equal(result.summary.billableTotal, 480000);
  assert.equal(result.summary.awaitingApproval, 2);
  assert.equal(result.summary.openRequests, 2);
});

test("updates a known request status and rejects unknown ids", () => {
  assert.equal(updateStatus([request()], "req-1", "approved")[0].status, "approved");
  assert.throws(() => updateStatus([request()], "missing", "done"), ValidationError);
});
