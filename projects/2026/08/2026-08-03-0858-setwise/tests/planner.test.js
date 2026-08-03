const test = require("node:test");
const assert = require("node:assert/strict");
const { ValidationError, normalizePiece, priorityScore, buildQueue, completePractice, summary, daysBetween } = require("../app/planner.js");

const today = "2026-08-03";
const piece = (overrides = {}) => ({
  id: "piece-a", title: "Etude A", section: "Bars 8-16", confidence: 3, minutes: 15,
  lastPracticed: "2026-07-30", performanceDate: "2026-08-12", ...overrides,
});

test("normalizes text and numeric fields", () => {
  const result = normalizePiece(piece({ title: "  Etude   A  ", confidence: "3", minutes: "15" }));
  assert.equal(result.title, "Etude A");
  assert.equal(result.confidence, 3);
  assert.equal(result.minutes, 15);
});

test("rejects invalid confidence and practice minutes", () => {
  assert.throws(() => normalizePiece(piece({ confidence: 0 })), ValidationError);
  assert.throws(() => normalizePiece(piece({ minutes: 121 })), ValidationError);
});

test("calculates calendar day distance", () => {
  assert.equal(daysBetween("2026-08-03", "2026-08-12"), 9);
});

test("gives weak and neglected pieces a higher priority", () => {
  const weak = priorityScore(piece({ confidence: 1, lastPracticed: "2026-07-20" }), today);
  const strong = priorityScore(piece({ confidence: 5, lastPracticed: "2026-08-02" }), today);
  assert.ok(weak > strong);
});

test("raises priority as a performance approaches", () => {
  const soon = priorityScore(piece({ performanceDate: "2026-08-05" }), today);
  const later = priorityScore(piece({ performanceDate: "2026-09-20" }), today);
  assert.ok(soon > later);
});

test("builds a ranked queue within the time budget", () => {
  const result = buildQueue([
    piece({ id: "weak", confidence: 1, minutes: 20 }),
    piece({ id: "strong", confidence: 5, minutes: 20, lastPracticed: "2026-08-02" }),
  ], 25, today);
  assert.equal(result.queue[0].id, "weak");
  assert.equal(result.plannedMinutes, 25);
  assert.equal(result.queue[1].plannedMinutes, 5);
});

test("completes a session and updates confidence and history", () => {
  const result = completePractice([piece()], [], { pieceId: "piece-a", confidence: 4, actualMinutes: 17, practicedOn: today });
  assert.equal(result.pieces[0].confidence, 4);
  assert.equal(result.pieces[0].lastPracticed, today);
  assert.equal(result.history[0].actualMinutes, 17);
});

test("summarizes repertoire, upcoming events, and weekly minutes", () => {
  const result = summary([piece(), piece({ id: "piece-b", performanceDate: "2026-09-20" })], [
    { practicedOn: "2026-08-01", actualMinutes: 20 }, { practicedOn: "2026-07-20", actualMinutes: 99 },
  ], today);
  assert.deepEqual(result, { repertoire: 2, dueSoon: 1, weekMinutes: 20 });
});
