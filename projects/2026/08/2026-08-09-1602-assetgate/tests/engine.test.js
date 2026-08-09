const test=require('node:test'),assert=require('node:assert/strict'),E=require('../app/engine.js');const base={id:'x',project:'사이트 리뉴얼',client:'모노 스튜디오',item:'최종 로고',category:'브랜드 자료',dueDate:'2026-08-12',delayDays:3,status:'waiting'};
test('입력을 정규화한다',()=>assert.equal(E.normalize({...base,item:' <로고 원본> '}).item,'로고 원본'));
test('짧은 프로젝트명을 거부한다',()=>assert.throws(()=>E.normalize({...base,project:'웹'})));
test('예상 지연 범위를 검증한다',()=>assert.throws(()=>E.normalize({...base,delayDays:61})));
test('마감 초과를 판정한다',()=>assert.equal(E.enrich({...base,dueDate:'2026-08-08'},'2026-08-09').risk,'overdue'));
test('48시간 이내는 긴급이다',()=>assert.equal(E.enrich({...base,dueDate:'2026-08-11'},'2026-08-09').risk,'urgent'));
test('대시보드가 잠재 지연을 합산한다',()=>assert.equal(E.dashboard([base,{...base,id:'y',delayDays:2}],'2026-08-09').delayDays,5));
test('수신 완료를 토글한다',()=>assert.equal(E.markReceived([base],'x')[0].status,'received'));
test('프로젝트 준비도를 계산한다',()=>assert.equal(E.readiness([base,{...base,id:'y',status:'received'}],'사이트 리뉴얼'),50));
