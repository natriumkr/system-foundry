import { dashboard } from '../app/engine.js';
import { writeFile } from 'node:fs/promises';

const credits = [
  { reference:'MK-1042', learner:'Minseo Kim', course:'Piano intermediate', issuedDate:'2026-07-20', expiryDate:'2026-08-18', sessions:2, usedSessions:0, sessionValueKrw:45000, status:'open' },
  { reference:'MK-1047', learner:'Jiwon Park', course:'Watercolor basics', issuedDate:'2026-08-01', expiryDate:'2026-08-29', sessions:3, usedSessions:1, sessionValueKrw:38000, status:'open' },
  { reference:'MK-1051', learner:'Hyeon Lee', course:'English conversation', issuedDate:'2026-08-10', expiryDate:'2026-09-20', sessions:1, usedSessions:0, sessionValueKrw:32000, status:'open' },
  { reference:'MK-1033', learner:'Sora Choi', course:'Violin beginner', issuedDate:'2026-07-02', expiryDate:'2026-08-10', sessions:2, usedSessions:2, sessionValueKrw:42000, status:'completed' },
];
const data = dashboard(credits, '2026-08-15');
const won = (value) => `KRW ${Math.round(value).toLocaleString('en-US')}`;
const labels = { overdue:'EXPIRED', urgent:'URGENT', watch:'WATCH', ready:'AVAILABLE', closed:'CLOSED' };
const colors = { overdue:'#a3483e', urgent:'#a3483e', watch:'#a76b1b', ready:'#34745d', closed:'#68746f' };
const pales = { overdue:'#f2d9d5', urgent:'#f2d9d5', watch:'#f6e3c8', ready:'#dfeee8', closed:'#edf0ef' };
const rows = data.analyses.map((item, index) => {
  const y = 625 + index * 145;
  const status = item.risk === 'closed' ? 'Settled' : item.days < 0 ? `${Math.abs(item.days)}d late` : `${item.days}d left`;
  return `<rect x="500" y="${y}" width="780" height="122" rx="18" fill="#fff" stroke="#d4dad8"/>
  <rect x="525" y="${y+44}" width="90" height="30" rx="15" fill="${pales[item.risk]}"/><text x="550" y="${y+64}" class="tag" fill="${colors[item.risk]}">${labels[item.risk]}</text>
  <text x="640" y="${y+45}" class="item">${item.credit.learner} · ${item.credit.reference}</text><text x="640" y="${y+73}" class="muted">${item.credit.course} · expires ${item.credit.expiryDate}</text>
  <text x="1020" y="${y+47}" class="score">${item.remaining} session${item.remaining===1?'':'s'}</text><text x="1020" y="${y+75}" class="muted">${item.liability ? won(item.liability) : 'Settled'}</text><text x="1195" y="${y+60}" class="time">${status}</text>`;
}).join('\n');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1500"><style>.title{font:700 58px Arial;fill:#212a28}.sub{font:20px Arial;fill:#4d5955}.eye{font:700 13px Arial;letter-spacing:3px;fill:#315d72}.label{font:14px Arial;fill:#68746f}.metric{font:700 30px Arial;fill:#212a28}.h2{font:700 25px Arial;fill:#212a28}.field{font:700 13px Arial;fill:#34423d}.value{font:16px Arial;fill:#212a28}.tag{font:700 11px Arial}.item{font:700 17px Arial;fill:#212a28}.muted{font:13px Arial;fill:#68746f}.score{font:700 17px Arial;fill:#315d72}.time{font:700 14px Arial;fill:#212a28}</style>
<rect width="1440" height="1500" fill="#f5f2ec"/><text x="160" y="85" class="eye">EVERY MISSED CLASS HAS A PROMISE.</text><text x="160" y="150" class="title">MakeupLedger</text><text x="160" y="190" class="sub">Keep replacement-session promises visible before they expire.</text><rect x="1080" y="70" width="200" height="44" rx="22" fill="#e3eef2"/><text x="1110" y="98" class="tag" fill="#315d72">LOCAL-FIRST · SINGLE STUDIO</text><line x1="160" y1="235" x2="1280" y2="235" stroke="#d4dad8"/>
${[['Open credits',data.openCredits],['Sessions owed',data.sessions],['Outstanding value',won(data.liability)],['Need attention',data.dueSoon]].map((m,i)=>`<rect x="${160+i*290}" y="270" width="270" height="112" rx="17" fill="#fff" stroke="#d4dad8"/><text x="${182+i*290}" y="310" class="label">${m[0]}</text><text x="${182+i*290}" y="354" class="metric">${m[1]}</text>`).join('')}
<rect x="160" y="425" width="310" height="650" rx="18" fill="#fff" stroke="#d4dad8"/><text x="185" y="475" class="h2">Issue make-up credit</text>${[['Reference','MK-1058'],['Learner / course','Eunji · Vocal class'],['Issue / expiry','2026-08-15 / 2026-09-15'],['Sessions / value','2 / KRW 40,000']].map((m,i)=>`<text x="185" y="${520+i*92}" class="field">${m[0]}</text><rect x="185" y="${535+i*92}" width="260" height="46" rx="9" fill="#fff" stroke="#c8cfcc"/><text x="200" y="${564+i*92}" class="value">${m[1]}</text>`).join('')}<rect x="185" y="910" width="260" height="48" rx="9" fill="#315d72"/><text x="268" y="940" font-family="Arial" font-size="15" font-weight="700" fill="#fff">SAVE CREDIT</text><text x="185" y="995" class="muted">Use a non-sensitive learner label.</text>
<text x="500" y="455" class="eye">FULFILMENT QUEUE</text><text x="500" y="493" class="h2">Promises that need a booking</text><text x="1090" y="493" class="label">Expired and near-expiry first</text>${rows}<text x="500" y="1245" class="muted">Rendered from the same calculation engine verified by automated tests.</text></svg>`;
await writeFile(new URL('../tmp/dashboard.svg', import.meta.url), svg);
console.log(JSON.stringify({ openCredits:data.openCredits, sessions:data.sessions, liability:data.liability, dueSoon:data.dueSoon, firstRisk:data.analyses[0].risk }));
