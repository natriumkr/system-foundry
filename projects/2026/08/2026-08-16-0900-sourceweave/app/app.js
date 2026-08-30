import { SOURCE_TYPES, addClaim, addSource, dashboard, linkSource } from './engine.js';

const KEY = 'sourceweave-v1';
const seed = {
  sources: [
    { id:'S-01', title:'UNESCO AI and education guidance', url:'https://unesco.org/ai-education', type:'official', credibility:5 },
    { id:'S-02', title:'Peer-reviewed learning study', url:'https://doi.org/10.1000/example', type:'paper', credibility:5 },
    { id:'S-03', title:'University research briefing', url:'https://example.edu/research-brief', type:'official', credibility:4 },
  ],
  claims: [
    { id:'C-01', text:'Structured feedback can improve revision quality.', importance:5, sourceIds:['S-01','S-02'] },
    { id:'C-02', text:'Students need transparent criteria when AI tools are used.', importance:4, sourceIds:['S-01'] },
    { id:'C-03', text:'The proposed method reduces preparation time by 30%.', importance:5, sourceIds:[] },
    { id:'C-04', text:'A small pilot can reveal usability barriers.', importance:3, sourceIds:['S-03'] },
  ],
};
let state = JSON.parse(localStorage.getItem(KEY) || 'null') || seed;
const $ = (selector) => document.querySelector(selector);
const save = () => localStorage.setItem(KEY, JSON.stringify(state));
const statusLabel = { gap:'Needs evidence', supported:'One-source', strong:'Cross-checked' };
$('#sourceType').innerHTML = SOURCE_TYPES.map((type) => `<option value="${type}">${type}</option>`).join('');

function render() {
  const data = dashboard(state.claims, state.sources);
  $('#claims').textContent = data.claims; $('#sources').textContent = data.sources; $('#supported').textContent = data.supported; $('#gaps').textContent = data.gaps;
  const sourceOptions = state.sources.map((source) => `<option value="${source.id}">${source.id} · ${source.title}</option>`).join('');
  $('#queue').innerHTML = data.analyses.map(({ claim, linked, independent, average, status }) => `<article class="claim ${status}">
    <span class="badge">${statusLabel[status]}</span><div><h3>${claim.id} · ${claim.text}</h3><p>Importance ${claim.importance}/5 · ${linked.length} source${linked.length===1?'':'s'} · ${independent} domain${independent===1?'':'s'} · credibility ${average || '—'}</p></div>
    <select data-claim="${claim.id}"><option value="">Link source…</option>${sourceOptions}</select><button data-link="${claim.id}">Attach</button></article>`).join('');
  document.querySelectorAll('[data-link]').forEach((button) => button.addEventListener('click', () => {
    const select = document.querySelector(`[data-claim="${button.dataset.link}"]`);
    if (!select.value) return;
    state.claims = linkSource(state.claims, button.dataset.link, select.value, state.sources); save(); render();
  }));
}

$('#sourceForm').addEventListener('submit', (event) => { event.preventDefault(); try { state.sources = addSource(state.sources, Object.fromEntries(new FormData(event.currentTarget))); save(); event.currentTarget.reset(); $('#message').textContent='Source saved.'; render(); } catch(error) { $('#message').textContent=error.message; } });
$('#claimForm').addEventListener('submit', (event) => { event.preventDefault(); try { state.claims = addClaim(state.claims, Object.fromEntries(new FormData(event.currentTarget))); save(); event.currentTarget.reset(); $('#claimMessage').textContent='Claim saved.'; render(); } catch(error) { $('#claimMessage').textContent=error.message; } });
render();
