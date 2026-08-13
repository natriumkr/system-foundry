(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.BoxEngine=api})(typeof globalThis!=='undefined'?globalThis:this,function(){
  const ROOMS=['거실','주방','침실','서재','욕실','창고','기타'];
  const clean=(v,n=120)=>String(v??'').trim().replace(/[<>]/g,'').slice(0,n);
  const uid=()=>Math.random().toString(36).slice(2,10);
  function normalize(raw){
    const code=clean(raw.code,20).toUpperCase(),room=clean(raw.room,20),contents=clean(raw.contents,160);
    if(!/^[A-Z0-9-]{2,20}$/.test(code))throw Error('상자 코드는 영문·숫자·하이픈 2~20자로 입력하세요.');
    if(!ROOMS.includes(room))throw Error('도착 방을 선택하세요.');
    if(contents.length<2)throw Error('내용물을 2자 이상 입력하세요.');
    return{id:clean(raw.id)||uid(),code,room,contents,fragile:raw.fragile===true||raw.fragile==='on',status:'packed'};
  }
  function search(items,query){const q=clean(query,60).toLocaleLowerCase('ko-KR');if(!q)return [...items];return items.filter(x=>[x.code,x.room,x.contents].some(v=>String(v).toLocaleLowerCase('ko-KR').includes(q)));}
  function dashboard(items){const rows=[...items].sort((a,b)=>Number(b.fragile)-Number(a.fragile)||a.room.localeCompare(b.room,'ko'));const unpacked=rows.filter(x=>x.status==='unpacked').length;return{boxes:rows.length,fragile:rows.filter(x=>x.fragile&&x.status!=='unpacked').length,remaining:rows.length-unpacked,progress:rows.length?Math.round(unpacked/rows.length*100):0,rows};}
  function add(items,raw){const item=normalize(raw);if(items.some(x=>x.code===item.code))throw Error('이미 사용 중인 상자 코드입니다.');return[...items,item];}
  function toggle(items,id){if(!items.some(x=>x.id===id))throw Error('상자 기록을 찾을 수 없습니다.');return items.map(x=>x.id===id?{...x,status:x.status==='unpacked'?'packed':'unpacked'}:x);}
  return{ROOMS,normalize,search,dashboard,add,toggle};
});
