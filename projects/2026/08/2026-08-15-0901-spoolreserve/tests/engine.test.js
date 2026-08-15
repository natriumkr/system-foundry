import test from 'node:test';
import assert from 'node:assert/strict';
import { addSpool, analyze, consume, dashboard, normalizeJob, normalizeSpool, remainingG, remainingValue, requiredWithMargin } from '../app/engine.js';

const spool = normalizeSpool({ id: ' pla-blk-01 ', color: 'Matte Black', material: 'pla', tareG: 250, grossG: 850, purchaseG: 1000, priceKrw: 20000 });
const job = normalizeJob({ name: 'Case', material: 'PLA', requiredG: 180, safetyPct: 10 });

test('normalizes spool code and material', () => assert.equal(spool.id, 'PLA-BLK-01'));
test('rejects gross weight below tare', () => assert.throws(() => normalizeSpool({ ...spool, grossG: 100 })));
test('calculates real filament remaining', () => assert.equal(remainingG(spool), 600));
test('calculates proportional stock value', () => assert.equal(remainingValue(spool), 12000));
test('adds safety margin rounded up', () => assert.equal(requiredWithMargin(job), 199));
test('marks a compatible spool as fitting', () => assert.equal(analyze(spool, job).fits, true));
test('rejects another material', () => assert.equal(analyze({ ...spool, material: 'PETG' }, job).fits, false));
test('sorts fitting spools first', () => assert.equal(dashboard([{ ...spool, grossG: 400 }, spool], job).analyses[0].fits, true));
test('prevents duplicate spool codes', () => assert.throws(() => addSpool([spool], spool)));
test('records consumption against gross weight', () => assert.equal(remainingG(consume([spool], spool.id, 180)[0]), 420));
