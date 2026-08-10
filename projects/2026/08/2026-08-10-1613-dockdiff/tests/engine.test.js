const test=require('node:test'),assert=require('node:assert/strict'),E=require('../app/engine.js');const base={id:'x',supplier:'한빛 유통',item:'원두 1kg',invoice:'PO-12',deliveryDate:'2026-08-05',ordered:10,received:8,unitPrice:20000,claimDays:7,status:'open'};
test('날짜를 더한다',()=>assert.equal(E.addDays('2026-08-05',7),'2026-08-12'));
test('입력을 정규화한다',()=>assert.equal(E.normalize({...base,item:' <원두> '}).item,'원두'));
test('실수령 초과를 거부한다',()=>assert.throws(()=>E.normalize({...base,received:11})));
test('이의 기한 범위를 검증한다',()=>assert.throws(()=>E.normalize({...base,claimDays:31})));
test('부족 금액을 계산한다',()=>assert.equal(E.enrich(base,'2026-08-10').amount,40000));
test('48시간 이내는 긴급이다',()=>assert.equal(E.enrich(base,'2026-08-10').risk,'urgent'));
test('대시보드는 회수액을 합산한다',()=>assert.equal(E.dashboard([base,{...base,id:'y',received:9}],'2026-08-10').recovery,60000));
test('처리 완료를 토글한다',()=>assert.equal(E.resolve([base],'x')[0].status,'resolved'));
