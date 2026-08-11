const test=require('node:test'),assert=require('node:assert/strict'),E=require('../app/engine.js');const base={id:'x',area:'카운터',task:'시재 대조',owner:'민서',dueTime:'16:20',severity:3,status:'open'};
test('입력을 정규화한다',()=>assert.equal(E.normalize({...base,task:' <시재 대조> '}).task,'시재 대조'));
test('잘못된 시간을 거부한다',()=>assert.throws(()=>E.normalize({...base,dueTime:'25:10'})));
test('중요도 범위를 검증한다',()=>assert.throws(()=>E.normalize({...base,severity:4})));
test('30분 이내 항목은 긴급이다',()=>assert.equal(E.enrich(base,'2026-08-11T16:00').risk,'urgent'));
test('기한 초과를 계산한다',()=>assert.equal(E.enrich({...base,dueTime:'15:50'},'2026-08-11T16:00').risk,'overdue'));
test('중요한 항목이 높은 점수를 받는다',()=>assert.ok(E.enrich(base,'2026-08-11T16:00').score>E.enrich({...base,severity:1,dueTime:'18:00'},'2026-08-11T16:00').score));
test('완료율을 계산한다',()=>assert.equal(E.dashboard([base,{...base,id:'y',status:'done'}],'2026-08-11T16:00').completion,50));
test('완료 상태를 토글한다',()=>assert.equal(E.toggle([base],'x')[0].status,'done'));
