const test=require('node:test');const assert=require('node:assert/strict');const E=require('../app/engine.js');const people=['민준','서연','지우','도윤'];const expense={id:'a',title:'숙소',payer:'민준',amount:240000,members:people};
test('normalizes unique participants',()=>assert.deepEqual(E.normalizePeople(people),people));
test('rejects duplicate participants',()=>assert.throws(()=>E.normalizePeople(['민준','민준'])));
test('rejects invalid expense amount',()=>assert.throws(()=>E.normalizeExpense({...expense,amount:-1},people)));
test('rejects payer outside trip',()=>assert.throws(()=>E.normalizeExpense({...expense,payer:'다른사람'},people)));
test('splits one expense exactly',()=>assert.deepEqual(E.balances(people,[expense]),{민준:180000,서연:-60000,지우:-60000,도윤:-60000}));
test('distributes indivisible remainder without losing won',()=>{const b=E.balances(['가','나','다'],[{id:'x',title:'간식',payer:'가',amount:100,members:['가','나','다']}]);assert.equal(Object.values(b).reduce((a,c)=>a+c,0),0)});
test('creates balanced settlement transfers',()=>{const x=E.settlements({민준:146000,서연:6000,지우:-58000,도윤:-94000});assert.equal(x.reduce((s,t)=>s+t.amount,0),152000);assert.equal(x.length,3)});
test('summarizes total and transfers',()=>{const s=E.summary(people,[expense,{id:'b',title:'저녁',payer:'서연',amount:88000,members:people}]);assert.equal(s.total,328000);assert.ok(s.settlements.length>0)});
