const E=window.BoxEngine,KEY='boxbridge.items.v1';
const seed=[
  {id:'x1',code:'LIV-01',room:'거실',contents:'멀티탭, 공유기, 리모컨',fragile:false,status:'packed'},
  {id:'x2',code:'KIT-01',room:'주방',contents:'머그컵, 유리 밀폐용기',fragile:true,status:'packed'},
  {id:'x3',code:'BED-01',room:'침실',contents:'침구, 커튼, 수건',fragile:false,status:'unpacked'},
  {id:'x4',code:'STU-01',room:'서재',contents:'노트, 충전 케이블, 문구',fragile:false,status:'packed'}
];
let items;try{items=JSON.parse(localStorage.getItem(KEY))||seed}catch{items=seed}
const $=id=>document.getElementById(id),esc=s=>String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
function save(){localStorage.setItem(KEY,JSON.stringify(items))}
function render(){
  const d=E.dashboard(items),rows=E.search(d.rows,$('search').value);
  $('boxCount').textContent=d.boxes;$('fragileCount').textContent=d.fragile;$('remainingCount').textContent=d.remaining;$('progress').textContent=`${d.progress}%`;
  $('resultCount').textContent=`${rows.length}개 표시`;
  $('queue').innerHTML=rows.map(x=>`<article class="item ${x.status}"><span class="badge ${x.fragile?'high':'stable'}">${x.fragile?'깨짐주의':'일반'}</span><div><h3>${esc(x.code)} · ${esc(x.room)}</h3><p>${esc(x.contents)}</p></div><div class="score"><b>${x.status==='unpacked'?'정리 완료':'포장됨'}</b><small>${x.room} 도착</small></div><button data-id="${x.id}">${x.status==='unpacked'?'되돌리기':'정리 완료'}</button></article>`).join('')||'<p class="empty">검색 결과가 없습니다.</p>';
}
$('boxForm').addEventListener('submit',e=>{e.preventDefault();$('message').textContent='';try{items=E.add(items,Object.fromEntries(new FormData(e.currentTarget)));save();e.currentTarget.reset();render();$('message').textContent='상자 기록을 저장했습니다.'}catch(err){$('message').textContent=err.message}});
$('search').addEventListener('input',render);
$('queue').addEventListener('click',e=>{if(!e.target.dataset.id)return;items=E.toggle(items,e.target.dataset.id);save();render()});
render();
