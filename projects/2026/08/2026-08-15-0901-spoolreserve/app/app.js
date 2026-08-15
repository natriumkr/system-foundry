import { MATERIALS, addSpool, consume, dashboard, normalizeJob, remainingG, remainingValue } from './engine.js';

const KEY = 'spoolreserve-v1';
const seed = [
  { id: 'PLA-BLK-01', color: 'Matte Black', material: 'PLA', tareG: 248, grossG: 893, purchaseG: 1000, priceKrw: 22000, status: 'active' },
  { id: 'PLA-WHT-02', color: 'Pearl White', material: 'PLA', tareG: 240, grossG: 458, purchaseG: 1000, priceKrw: 24500, status: 'active' },
  { id: 'PETG-CLR-01', color: 'Clear', material: 'PETG', tareG: 252, grossG: 1080, purchaseG: 1000, priceKrw: 28000, status: 'active' },
];
let spools = JSON.parse(localStorage.getItem(KEY) || 'null') || seed;
let job = normalizeJob({ name: 'Enclosure set', material: 'PLA', requiredG: 180, safetyPct: 12 });

const $ = (selector) => document.querySelector(selector);
const won = (value) => `₩${Math.round(value).toLocaleString('en-US')}`;
const save = () => localStorage.setItem(KEY, JSON.stringify(spools));
const options = MATERIALS.map((item) => `<option>${item}</option>`).join('');
$('#material').innerHTML = options;
$('#jobMaterial').innerHTML = options;

function render() {
  const data = dashboard(spools, job);
  $('#count').textContent = data.spools;
  $('#grams').textContent = `${Math.round(data.grams)}g`;
  $('#value').textContent = won(data.value);
  $('#matches').textContent = data.matches;
  $('#needed').textContent = `${data.analyses[0]?.needed || 0}g incl. margin`;
  $('#list').innerHTML = data.analyses.map(({ spool, remaining, needed, fits, shortage, runs }) => `
    <article class="spool ${fits ? 'fit' : ''}">
      <div class="dot" style="background:${spool.color.toLowerCase().includes('black') ? '#252b2a' : spool.color.toLowerCase().includes('white') ? '#e9e7df' : '#b8d7d0'}"></div>
      <div><span class="tag">${spool.material}</span><h3>${spool.color} · ${spool.id}</h3><p>${remaining}g left · ${won(remainingValue(spool))} stock value</p></div>
      <div class="decision"><b>${fits ? `${runs} run${runs === 1 ? '' : 's'}` : shortage === null ? 'Other material' : `${shortage}g short`}</b><small>${needed}g needed</small></div>
      <button data-id="${spool.id}" ${fits ? '' : 'disabled'}>Use ${job.requiredG}g</button>
    </article>`).join('');
  document.querySelectorAll('[data-id]').forEach((button) => button.addEventListener('click', () => {
    spools = consume(spools, button.dataset.id, job.requiredG); save(); render();
  }));
}

$('#spoolForm').addEventListener('submit', (event) => {
  event.preventDefault();
  try {
    const values = Object.fromEntries(new FormData(event.currentTarget));
    spools = addSpool(spools, values); save(); event.currentTarget.reset(); $('#message').textContent = 'Spool saved.'; render();
  } catch (error) { $('#message').textContent = error.message; }
});

$('#jobForm').addEventListener('submit', (event) => {
  event.preventDefault();
  try { job = normalizeJob(Object.fromEntries(new FormData(event.currentTarget))); $('#jobMessage').textContent = 'Match updated.'; render(); }
  catch (error) { $('#jobMessage').textContent = error.message; }
});

render();
