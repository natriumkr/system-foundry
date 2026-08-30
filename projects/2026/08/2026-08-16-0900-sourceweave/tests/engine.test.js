import test from 'node:test';
import assert from 'node:assert/strict';
import { addClaim, addSource, analyzeClaim, dashboard, linkSource, normalizeClaim, normalizeSource } from '../app/engine.js';

const s1 = normalizeSource({ id:' s-1 ', title:'Official guidance', url:'https://agency.example/guidance', type:'official', credibility:5 });
const s2 = normalizeSource({ id:'S-2', title:'Research paper', url:'https://journal.example/paper', type:'paper', credibility:4 });
const claim = normalizeClaim({ id:' c-1 ', text:'Structured feedback improves revision.', importance:5, sourceIds:['S-1'] });
test('normalizes source ID and type', () => assert.equal(s1.id, 'S-1'));
test('rejects non-HTTPS source URL', () => assert.throws(() => normalizeSource({ ...s1, url:'http://example.com' })));
test('deduplicates linked source IDs', () => assert.deepEqual(normalizeClaim({ ...claim, sourceIds:['S-1','S-1'] }).sourceIds, ['S-1']));
test('marks claim without sources as gap', () => assert.equal(analyzeClaim({ ...claim, sourceIds:[] }, [s1]).status, 'gap'));
test('marks single-source claim supported', () => assert.equal(analyzeClaim(claim, [s1]).status, 'supported'));
test('marks two strong independent sources cross-checked', () => assert.equal(analyzeClaim({ ...claim, sourceIds:['S-1','S-2'] }, [s1,s2]).status, 'strong'));
test('dashboard counts evidence gaps', () => assert.equal(dashboard([claim,{ ...claim,id:'C-2',sourceIds:[] }],[s1]).gaps, 1));
test('prevents duplicate source IDs', () => assert.throws(() => addSource([s1], s1)));
test('prevents duplicate claim IDs', () => assert.throws(() => addClaim([claim], claim)));
test('links an existing source once', () => assert.deepEqual(linkSource([claim],claim.id,s2.id,[s1,s2])[0].sourceIds,['S-1','S-2']));
