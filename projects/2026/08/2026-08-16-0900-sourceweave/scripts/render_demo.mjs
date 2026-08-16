import { dashboard, normalizeClaim, normalizeSource } from '../app/engine.js';
import { writeFile } from 'node:fs/promises';

const sources = [
  normalizeSource({ id: 'S-01', title: 'Primary field study', url: 'https://doi.org/10.1000/field-study', type: 'paper', credibility: 5 }),
  normalizeSource({ id: 'S-02', title: 'National research bulletin', url: 'https://research.example.org/bulletin', type: 'official', credibility: 5 }),
  normalizeSource({ id: 'S-03', title: 'Methods handbook', url: 'https://books.example.net/methods', type: 'book', credibility: 4 }),
];
const claims = [
  normalizeClaim({ id: 'C-01', text: 'The observed effect appears consistently across independent datasets.', importance: 5, sourceIds: ['S-01', 'S-02'] }),
  normalizeClaim({ id: 'C-02', text: 'The selected method is suitable for the target sample size.', importance: 4, sourceIds: ['S-03'] }),
  normalizeClaim({ id: 'C-03', text: 'The intervention remains effective after six months.', importance: 5, sourceIds: [] }),
  normalizeClaim({ id: 'C-04', text: 'The measurement protocol can be reproduced by another team.', importance: 3, sourceIds: ['S-01'] }),
];
const metrics = dashboard(claims, sources);
const esc = (value) => String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[char]));
const cards = metrics.analyses.map((item, index) => {
  const y = 518 + index * 180;
  const palette = item.status === 'gap' ? ['#FFF1E8', '#C95C28', 'Evidence gap'] : item.status === 'strong' ? ['#E7F6EF', '#16765D', 'Cross-checked'] : ['#EEF2FF', '#4457B8', 'Single source'];
  return `<g><rect x="556" y="${y}" width="804" height="148" rx="20" fill="#FFFFFF" stroke="#DDE4E8"/>
    <rect x="584" y="${y + 24}" width="130" height="32" rx="16" fill="${palette[0]}"/><text x="649" y="${y + 46}" class="tag" fill="${palette[1]}" text-anchor="middle">${palette[2]}</text>
    <text x="584" y="${y + 86}" class="claim">${esc(item.claim.text)}</text>
    <text x="584" y="${y + 120}" class="meta">${item.claim.id} · importance ${item.claim.importance}/5 · ${item.linked.length} linked source${item.linked.length === 1 ? '' : 's'}</text>
    <text x="1326" y="${y + 46}" class="score" text-anchor="end">${item.priority}</text><text x="1326" y="${y + 67}" class="tiny" text-anchor="end">priority</text></g>`;
}).join('');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1320" viewBox="0 0 1440 1320">
<style>@font-face{font-family:Inter;src:local('DejaVu Sans')}text{font-family:Inter,'DejaVu Sans',sans-serif}.brand{font-size:31px;font-weight:700;fill:#F8FBFB}.eyebrow{font-size:13px;font-weight:700;letter-spacing:2px;fill:#9ADCC9}.hero{font-size:42px;font-weight:700;fill:#F8FBFB}.sub{font-size:17px;fill:#C4DAD4}.stat{font-size:31px;font-weight:700;fill:#132D2A}.label{font-size:13px;font-weight:600;fill:#657876}.panel{font-size:22px;font-weight:700;fill:#173632}.small{font-size:14px;fill:#607370}.field{font-size:13px;fill:#4C625F}.value{font-size:15px;fill:#203B37}.button{font-size:15px;font-weight:700;fill:#FFF}.tag{font-size:12px;font-weight:700}.claim{font-size:16px;font-weight:600;fill:#183632}.meta{font-size:13px;fill:#6A7B79}.score{font-size:21px;font-weight:700;fill:#21483F}.tiny{font-size:11px;fill:#82918F}</style>
<rect width="1440" height="1320" fill="#F5F7F6"/><rect width="1440" height="286" fill="#123A34"/>
<circle cx="90" cy="68" r="22" fill="#42B99A"/><path d="M78 68h24M90 56v24" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
<text x="130" y="79" class="brand">SourceWeave</text><text x="80" y="137" class="eyebrow">LOCAL-FIRST EVIDENCE WORKSPACE</text>
<text x="80" y="191" class="hero">Know which claim needs evidence next.</text><text x="80" y="231" class="sub">Connect claims to credible sources, expose gaps, and see cross-check status at a glance.</text>
<g transform="translate(80 318)"><rect width="280" height="130" rx="20" fill="#FFF"/><text x="26" y="45" class="label">CLAIMS</text><text x="26" y="91" class="stat">${metrics.claims}</text><text x="76" y="90" class="small">tracked</text></g>
<g transform="translate(378 318)"><rect width="280" height="130" rx="20" fill="#FFF"/><text x="26" y="45" class="label">SOURCES</text><text x="26" y="91" class="stat">${metrics.sources}</text><text x="76" y="90" class="small">verified URLs</text></g>
<g transform="translate(676 318)"><rect width="280" height="130" rx="20" fill="#FFF"/><text x="26" y="45" class="label">SUPPORTED</text><text x="26" y="91" class="stat">${metrics.supported}</text><text x="76" y="90" class="small">of ${metrics.claims} claims</text></g>
<g transform="translate(974 318)"><rect width="386" height="130" rx="20" fill="#FFF1E8"/><text x="26" y="45" class="label">ACTION NEEDED</text><text x="26" y="91" class="stat" fill="#B84E22">${metrics.gaps}</text><text x="76" y="90" class="small">evidence gap</text><rect x="260" y="33" width="96" height="54" rx="15" fill="#E7F6EF"/><text x="308" y="58" class="tag" fill="#16765D" text-anchor="middle">${metrics.strong} strong</text></g>
<g><rect x="80" y="488" width="436" height="730" rx="24" fill="#FFF" stroke="#DDE4E8"/><text x="112" y="536" class="panel">Add a source</text><text x="112" y="568" class="small">Credibility and HTTPS are checked before saving.</text>
<text x="112" y="620" class="field">SOURCE ID</text><rect x="112" y="638" width="372" height="50" rx="11" fill="#F7F9F8" stroke="#D8E0DE"/><text x="130" y="669" class="value">S-04</text>
<text x="112" y="728" class="field">TITLE</text><rect x="112" y="746" width="372" height="50" rx="11" fill="#F7F9F8" stroke="#D8E0DE"/><text x="130" y="777" class="value">Replication dataset</text>
<text x="112" y="836" class="field">HTTPS URL</text><rect x="112" y="854" width="372" height="50" rx="11" fill="#F7F9F8" stroke="#D8E0DE"/><text x="130" y="885" class="value">https://data.example.org/study</text>
<text x="112" y="944" class="field">TYPE</text><rect x="112" y="962" width="178" height="50" rx="11" fill="#F7F9F8" stroke="#D8E0DE"/><text x="130" y="993" class="value">Official</text><text x="306" y="944" class="field">CREDIBILITY</text><rect x="306" y="962" width="178" height="50" rx="11" fill="#F7F9F8" stroke="#D8E0DE"/><text x="324" y="993" class="value">5 / 5</text>
<rect x="112" y="1050" width="372" height="54" rx="13" fill="#207F6B"/><text x="298" y="1083" class="button" text-anchor="middle">Save source</text><rect x="112" y="1132" width="372" height="54" rx="13" fill="#EDF4F2"/><text x="298" y="1165" class="button" fill="#285C52" text-anchor="middle">Add a claim instead</text></g>
<text x="556" y="490" class="panel">Evidence queue</text><text x="1326" y="490" class="small" text-anchor="end">Gaps first · then single-source claims</text>${cards}
<text x="80" y="1272" class="small">Your research data stays in this browser. Export is planned for the next release.</text><text x="1360" y="1272" class="small" text-anchor="end">SourceWeave MVP · 2026-08-16</text>
</svg>`;
await writeFile(new URL('../tmp/dashboard.svg', import.meta.url), svg);
console.log(JSON.stringify({ claims: metrics.claims, sources: metrics.sources, supported: metrics.supported, strong: metrics.strong, gaps: metrics.gaps }));
