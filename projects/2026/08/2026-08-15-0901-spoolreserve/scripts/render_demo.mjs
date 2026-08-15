import { dashboard, normalizeJob } from '../app/engine.js';
import { writeFile } from 'node:fs/promises';

const spools = [
  { id: 'PLA-BLK-01', color: 'Matte Black', material: 'PLA', tareG: 248, grossG: 893, purchaseG: 1000, priceKrw: 22000, status: 'active' },
  { id: 'PLA-WHT-02', color: 'Pearl White', material: 'PLA', tareG: 240, grossG: 458, purchaseG: 1000, priceKrw: 24500, status: 'active' },
  { id: 'PETG-CLR-01', color: 'Clear', material: 'PETG', tareG: 252, grossG: 1080, purchaseG: 1000, priceKrw: 28000, status: 'active' },
];
const job = normalizeJob({ name: 'Enclosure set', material: 'PLA', requiredG: 180, safetyPct: 12 });
const data = dashboard(spools, job);
const won = (value) => `KRW ${Math.round(value).toLocaleString('en-US')}`;
const rows = data.analyses.map((item, index) => {
  const y = 700 + index * 150;
  const status = item.fits ? `${item.runs} complete runs` : item.shortage === null ? 'Other material' : `${item.shortage}g short`;
  const stroke = item.fits ? '#4a9b7f' : '#d4dcd8';
  return `<rect x="500" y="${y}" width="780" height="126" rx="18" fill="#fff" stroke="${stroke}" stroke-width="2"/>
  <circle cx="545" cy="${y + 63}" r="18" fill="${index === 0 ? '#252b2a' : index === 1 ? '#e9e7df' : '#b8d7d0'}"/>
  <text x="580" y="${y + 42}" class="tag">${item.spool.material}</text><text x="580" y="${y + 72}" class="item">${item.spool.color} · ${item.spool.id}</text>
  <text x="580" y="${y + 98}" class="muted">${item.remaining}g left · ${won(item.remaining / item.spool.purchaseG * item.spool.priceKrw)} stock value</text>
  <text x="1080" y="${y + 56}" class="score">${status}</text><text x="1080" y="${y + 84}" class="muted">${item.needed}g needed</text>`;
}).join('\n');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1500" viewBox="0 0 1440 1500">
<style>.title{font:700 58px Arial;fill:#1f2926}.sub{font:20px Arial;fill:#4d5b55}.eye{font:700 13px Arial;letter-spacing:3px;fill:#28775f}.label{font:14px Arial;fill:#65736d}.metric{font:700 30px Arial;fill:#1f2926}.h2{font:700 25px Arial;fill:#1f2926}.field{font:700 13px Arial;fill:#34423d}.value{font:16px Arial;fill:#1f2926}.tag{font:700 12px Arial;fill:#28775f}.item{font:700 17px Arial;fill:#1f2926}.muted{font:13px Arial;fill:#65736d}.score{font:700 18px Arial;fill:#28775f}</style>
<rect width="1440" height="1500" fill="#f5f2eb"/><text x="160" y="85" class="eye">KNOW BEFORE YOU PRINT.</text><text x="160" y="150" class="title">SpoolReserve</text><text x="160" y="190" class="sub">Match real filament weight to the next job, with safety margin included.</text>
<rect x="1080" y="70" width="200" height="44" rx="22" fill="#e0f0ea"/><text x="1115" y="98" class="tag">LOCAL DATA · NO ACCOUNT</text><line x1="160" y1="235" x2="1280" y2="235" stroke="#d4dcd8"/>
${[['Active spools',data.spools],['Filament left',`${data.grams}g`],['Stock value',won(data.value)],['Job matches',data.matches]].map((m,i)=>`<rect x="${160+i*290}" y="270" width="270" height="112" rx="17" fill="#fff" stroke="#d4dcd8"/><text x="${182+i*290}" y="310" class="label">${m[0]}</text><text x="${182+i*290}" y="354" class="metric">${m[1]}</text>`).join('')}
<rect x="160" y="425" width="310" height="650" rx="18" fill="#fff" stroke="#d4dcd8"/><text x="185" y="475" class="h2">Add a spool</text>
${[['Spool code','PLA-GRY-03'],['Material / color','PLA · Graphite'],['Gross / empty weight','910g / 245g'],['Purchased net / price','1000g / KRW 24,000']].map((m,i)=>`<text x="185" y="${520+i*92}" class="field">${m[0]}</text><rect x="185" y="${535+i*92}" width="260" height="46" rx="9" fill="#fff" stroke="#c8d0cc"/><text x="200" y="${564+i*92}" class="value">${m[1]}</text>`).join('')}
<rect x="185" y="910" width="260" height="48" rx="9" fill="#28775f"/><text x="275" y="940" font-family="Arial" font-size="15" font-weight="700" fill="#fff">SAVE SPOOL</text><text x="185" y="995" class="muted">Measured weight minus empty spool tare.</text>
<text x="500" y="455" class="eye">JOB FEASIBILITY</text><text x="500" y="493" class="h2">Choose the spool that can finish</text><text x="1125" y="493" class="label">202g incl. margin</text>
<rect x="500" y="525" width="780" height="140" rx="17" fill="#fff" stroke="#d4dcd8"/>${[['Job','Enclosure set'],['Material','PLA'],['Estimate','180g'],['Safety','12%']].map((m,i)=>`<text x="${525+i*180}" y="558" class="field">${m[0]}</text><rect x="${525+i*180}" y="570" width="155" height="47" rx="8" fill="#fff" stroke="#c8d0cc"/><text x="${540+i*180}" y="600" class="value">${m[1]}</text>`).join('')}<rect x="1065" y="625" width="190" height="28" rx="8" fill="#28775f"/><text x="1122" y="645" font-family="Arial" font-size="12" font-weight="700" fill="#fff">CHECK FIT</text>
${rows}<text x="500" y="1220" class="muted">Rendered from the same calculation engine verified by automated tests.</text></svg>`;
await writeFile(new URL('../tmp/dashboard.svg', import.meta.url), svg);
console.log(JSON.stringify({ spools: data.spools, grams: data.grams, value: data.value, matches: data.matches, needed: data.analyses[0].needed }));
