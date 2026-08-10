const test=require('node:test'),assert=require('node:assert/strict'),E=require('../app/engine.js');const device={id:'d',kind:'device',name:'업무 노트북',port:'USB-C',watts:65,travel:true},charger={id:'c',kind:'charger',name:'고출력 충전기',port:'USB-C',watts:100,travel:false};
test('입력을 정규화한다',()=>assert.equal(E.normalize({...device,name:' <노트북> '}).name,'노트북'));
test('짧은 장비명을 거부한다',()=>assert.throws(()=>E.normalize({...device,name:'폰'})));
test('출력 범위를 검증한다',()=>assert.throws(()=>E.normalize({...device,watts:301})));
test('충분한 출력은 호환된다',()=>assert.equal(E.matches(device,charger),true));
test('포트가 다르면 호환되지 않는다',()=>assert.equal(E.matches(device,{...charger,port:'USB-A'}),false));
test('출력이 낮으면 호환되지 않는다',()=>assert.equal(E.matches(device,{...charger,watts:30}),false));
test('분석이 미지원 기기를 센다',()=>assert.equal(E.analyze([device,{...device,id:'d2',port:'Lightning'},charger]).uncovered,1));
test('여행 포함을 토글한다',()=>assert.equal(E.toggleTravel([device],'d')[0].travel,false));
