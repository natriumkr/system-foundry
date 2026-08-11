const test=require('node:test'),assert=require('node:assert/strict'),E=require('../app/engine.js');const base={id:'x',subject:'수학',title:'확률 문제 풀이',dueDate:'2026-08-12',minutes:60,importance:5,status:'open'};
test('입력을 정규화한다',()=>assert.equal(E.normalize({...base,title:' <문제 풀이> '}).title,'문제 풀이'));
test('너무 짧은 학습 시간을 거부한다',()=>assert.throws(()=>E.normalize({...base,minutes:5})));
test('중요도 범위를 검증한다',()=>assert.throws(()=>E.normalize({...base,importance:6})));
test('하루 남은 할 일은 곧 마감이다',()=>assert.equal(E.enrich(base,'2026-08-11').urgency,'soon'));
test('중요한 가까운 일이 높은 점수를 받는다',()=>assert.ok(E.enrich(base,'2026-08-11').score>E.enrich({...base,importance:1,dueDate:'2026-08-20'},'2026-08-11').score));
test('시간 예산 안에서 계획을 만든다',()=>assert.deepEqual(E.dashboard([base,{...base,id:'y',minutes:70,importance:4}],'2026-08-11',60).todayPlan,['x']));
test('대시보드는 남은 시간을 합산한다',()=>assert.equal(E.dashboard([base,{...base,id:'y',minutes:30}],'2026-08-11').minutes,90));
test('완료 상태를 토글한다',()=>assert.equal(E.toggle([base],'x')[0].status,'done'));
