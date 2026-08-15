import test from 'node:test';
import assert from 'node:assert/strict';
import { addCredit, analyze, dashboard, daysUntil, liability, normalizeCredit, redeem, remainingSessions } from '../app/engine.js';

const credit = normalizeCredit({ reference:' mk-1 ', learner:'Minseo', course:'Piano', issuedDate:'2026-08-01', expiryDate:'2026-08-20', sessions:3, usedSessions:1, sessionValueKrw:40000, status:'open' });
test('normalizes reference', () => assert.equal(credit.reference, 'MK-1'));
test('rejects expiry before issue', () => assert.throws(() => normalizeCredit({ ...credit, expiryDate:'2026-07-31' })));
test('calculates remaining sessions', () => assert.equal(remainingSessions(credit), 2));
test('calculates outstanding value', () => assert.equal(liability(credit), 80000));
test('calculates days until expiry', () => assert.equal(daysUntil('2026-08-20', '2026-08-15'), 5));
test('classifies seven-day item urgent', () => assert.equal(analyze(credit, '2026-08-15').risk, 'urgent'));
test('classifies expired item overdue', () => assert.equal(analyze({ ...credit, expiryDate:'2026-08-10' }, '2026-08-15').risk, 'overdue'));
test('dashboard totals outstanding liability', () => assert.equal(dashboard([credit], '2026-08-15').liability, 80000));
test('prevents duplicate references', () => assert.throws(() => addCredit([credit], credit)));
test('redeems and completes the final session', () => assert.equal(redeem([{ ...credit, usedSessions:2 }], credit.reference)[0].status, 'completed'));
