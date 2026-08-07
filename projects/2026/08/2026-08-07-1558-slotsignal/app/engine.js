(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.SlotEngine=api})(typeof globalThis!=='undefined'?globalThis:this,function(){
  const services=['컷','컬러','클리닉','네일'];
  const periods=['morning','afternoon','evening'];
  const clean=(v,max=80)=>String(v??'').trim().replace(/[<>]/g,'').slice(0,max);
  const dateOk=v=>/^\d{4}-\d{2}-\d{2}$/.test(v)&&!Number.isNaN(Date.parse(v+'T00:00:00'));
  const timeOk=v=>/^([01]\d|2[0-3]):[0-5]\d$/.test(v);
  const uid=()=>Math.random().toString(36).slice(2,10);
  function normalizeCustomer(raw){const name=clean(raw.name,30),service=clean(raw.service,20),availability=clean(raw.availability,20),joined=clean(raw.joined,10);if(name.length<2)throw Error('고객명은 2자 이상 입력하세요.');if(!services.includes(service))throw Error('지원 서비스만 선택하세요.');if(!periods.includes(availability))throw Error('가능 시간대를 선택하세요.');if(!dateOk(joined))throw Error('등록일을 확인하세요.');return{id:clean(raw.id)||uid(),name,service,availability,joined,status:'waiting'}}
  function normalizeSlot(raw){const service=clean(raw.service,20),date=clean(raw.date,10),time=clean(raw.time,5),price=Number(raw.price);if(!services.includes(service))throw Error('지원 서비스만 선택하세요.');if(!dateOk(date)||!timeOk(time))throw Error('예약 날짜와 시간을 확인하세요.');if(!Number.isFinite(price)||price<1000||price>2000000)throw Error('예상 매출은 1,000~2,000,000원이어야 합니다.');return{id:clean(raw.id)||uid(),service,date,time,price:Math.round(price),status:'open'}}
  function periodFor(time){const h=Number(time.slice(0,2));return h<12?'morning':h<17?'afternoon':'evening'}
  function daysBetween(a,b){return Math.max(0,Math.floor((Date.parse(b+'T00:00:00')-Date.parse(a+'T00:00:00'))/86400000))}
  function score(customer,slot,today){if(customer.status!=='waiting'||slot.status!=='open'||customer.service!==slot.service)return 0;const availability=customer.availability===periodFor(slot.time)?35:0;const waiting=Math.min(25,daysBetween(customer.joined,today));const urgency=Math.max(0,20-Math.min(20,daysBetween(today,slot.date)));return 40+availability+waiting+urgency}
  function matchQueue(customers,slots,today){const rows=[];for(const slot of slots.filter(x=>x.status==='open'))for(const customer of customers.filter(x=>x.status==='waiting')){const matchScore=score(customer,slot,today);if(matchScore>=40)rows.push({...customer,slotId:slot.id,slotDate:slot.date,slotTime:slot.time,slotService:slot.service,slotPrice:slot.price,matchScore,periodMatch:customer.availability===periodFor(slot.time)})}return rows.sort((a,b)=>b.matchScore-a.matchScore||a.slotDate.localeCompare(b.slotDate))}
  function dashboard(customers,slots,today){const open=slots.filter(x=>x.status==='open');return{waitingCount:customers.filter(x=>x.status==='waiting').length,openCount:open.length,revenueAtRisk:open.reduce((s,x)=>s+x.price,0),queue:matchQueue(customers,slots,today)}}
  function fillSlot(customers,slots,slotId,customerId){if(!slots.some(x=>x.id===slotId&&x.status==='open'))throw Error('열린 슬롯을 찾을 수 없습니다.');if(!customers.some(x=>x.id===customerId&&x.status==='waiting'))throw Error('대기 고객을 찾을 수 없습니다.');return{customers:customers.map(x=>x.id===customerId?{...x,status:'booked'}:x),slots:slots.map(x=>x.id===slotId?{...x,status:'filled',customerId}:x)}}
  return{services,periods,normalizeCustomer,normalizeSlot,periodFor,score,matchQueue,dashboard,fillSlot};
});
