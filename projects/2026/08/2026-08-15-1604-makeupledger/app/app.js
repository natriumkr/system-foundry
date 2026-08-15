import { addCredit, dashboard, redeem } from './engine.js';

const KEY = 'makeupledger-v1';
const today = new Date().toISOString().slice(0, 10);
const seed = [
  { reference:'MK-1042', learner:'Minseo Kim', course:'Piano intermediate', issuedDate:'2026-07-20', expiryDate:'2026-08-18', sessions:2, usedSessions:0, sessionValueKrw:45000, status:'open' },
  { reference:'MK-1047', learner:'Jiwon Park', course:'Watercolor basics', issuedDate:'2026-08-01', expiryDate:'2026-08-29', sessions:3, usedSessions:1, sessionValueKrw:38000, status:'open' },
  { reference:'MK-1051', learner:'Hyeon Lee', course:'English conversation', issuedDate:'2026-08-10', expiryDate:'2026-09-20', sessions:1, usedSessions:0, sessionValueKrw:32000, status:'open' },
  { reference:'MK-1033', learner:'Sora Choi', course:'Violin beginner', issuedDate:'2026-07-02', expiryDate:'2026-08-10', sessions:2, usedSessions:2, sessionValueKrw:42000, status:'completed' },
];
let credits = JSON.parse(localStorage.getItem(KEY) || 'null') || seed;
const $ = (selector) => document.querySelector(selector);
const won = (value) => `₩${Math.round(value).toLocaleString('en-US')}`;
const save = () => localStorage.setItem(KEY, JSON.stringify(credits));
const label = { overdue:'Expired', urgent:'Urgent', watch:'Watch', ready:'Available', closed:'Closed' };

function render() {
  const data = dashboard(credits, today);
  $('#open').textContent = data.openCredits; $('#sessions').textContent = data.sessions; $('#liability').textContent = won(data.liability); $('#due').textContent = data.dueSoon;
  $('#queue').innerHTML = data.analyses.map(({ credit, remaining, days, risk, liability }) => `<article class="credit ${risk}">
    <span class="badge">${label[risk]}</span><div><h3>${credit.learner} · ${credit.reference}</h3><p>${credit.course} · expires ${credit.expiryDate}</p></div>
    <div class="metric"><b>${remaining} session${remaining === 1 ? '' : 's'}</b><small>${liability ? won(liability) : 'Settled'}</small></div>
    <div class="time"><b>${risk === 'closed' ? '—' : days < 0 ? `${Math.abs(days)}d late` : `${days}d left`}</b></div>
    <button data-ref="${credit.reference}" ${credit.status === 'open' && remaining ? '' : 'disabled'}>Redeem 1</button></article>`).join('');
  document.querySelectorAll('[data-ref]').forEach((button) => button.addEventListener('click', () => { credits = redeem(credits, button.dataset.ref); save(); render(); }));
}

$('#creditForm').addEventListener('submit', (event) => {
  event.preventDefault();
  try { credits = addCredit(credits, Object.fromEntries(new FormData(event.currentTarget))); save(); event.currentTarget.reset(); $('#message').textContent = 'Make-up credit saved.'; render(); }
  catch (error) { $('#message').textContent = error.message; }
});

render();
