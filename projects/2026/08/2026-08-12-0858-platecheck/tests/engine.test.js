const test=require('node:test'),assert=require('node:assert/strict'),E=require('../app/engine.js');const base={id:'x',name:'센서 브래킷',partW:72,partD:48,bedW:250,bedD:210,gap:6,needed:12,status:'planned'};
test('입력을 정규화한다',()=>assert.equal(E.normalize({...base,name:' <브래킷> '}).name,'브래킷'));
test('잘못된 부품 치수를 거부한다',()=>assert.throws(()=>E.normalize({...base,partW:0})));
test('간격 범위를 검증한다',()=>assert.throws(()=>E.normalize({...base,gap:31})));
test('격자 배치 용량을 계산한다',()=>assert.equal(E.capacity(100,100,30,30,5),9));
test('회전 배치 중 큰 용량을 선택한다',()=>assert.equal(E.analyze({...base,partW:100,partD:40,bedW:210,bedD:120,gap:5}).rotation,0));
test('출력판 초과를 판정한다',()=>assert.equal(E.analyze({...base,partW:260}).fits,false));
test('필요 출력판 수를 계산한다',()=>assert.equal(E.analyze(base).plates,1));
test('기록을 삭제한다',()=>assert.equal(E.remove([base],'x').length,0));
