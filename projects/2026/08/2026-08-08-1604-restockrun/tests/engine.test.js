const test=require('node:test'),assert=require('node:assert/strict'),E=require('../app/engine.js');const base={name:'PLA 필라멘트',category:'3D프린팅',unit:'롤',stock:4,dailyUse:.5,reorderPoint:2,unitCost:22000};
test('valid item normalizes numbers',()=>assert.equal(E.normalize({...base,stock:'4'}).stock,4));
test('short name is rejected',()=>assert.throws(()=>E.normalize({...base,name:'A'}),/2자/));
test('unsupported category is rejected',()=>assert.throws(()=>E.normalize({...base,category:'식품'}),/카테고리/));
test('negative stock is rejected',()=>assert.throws(()=>E.normalize({...base,stock:-1}),/현재 수량/));
test('zero daily usage is rejected',()=>assert.throws(()=>E.normalize({...base,dailyUse:0}),/0보다/));
test('critical item gets suggested order',()=>{const x=E.enrich({...base,stock:2});assert.equal(x.risk,'critical');assert.equal(x.suggested,2);assert.equal(x.reorderCost,44000)});
test('dashboard sorts runway and totals budget',()=>{const a={id:'a',...base,status:'active'},b={id:'b',...base,stock:1,status:'active'};const d=E.dashboard([a,b]);assert.equal(d.rows[0].id,'b');assert.equal(d.critical,1);assert.equal(d.budget,66000)});
test('usage decrements without negative stock',()=>{const x=[{id:'a',stock:.5}],r=E.use(x,'a',1);assert.equal(r[0].stock,0);assert.throws(()=>E.use(x,'a',0),/사용량/)});
