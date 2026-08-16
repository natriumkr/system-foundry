const clean = (v, max = 160) => String(v ?? '').trim().replace(/[<>"'&]/g, '').slice(0, max);
const number = (v, label, min, max) => { const n = Number(v); if (!Number.isFinite(n) || n < min || n > max) throw new Error(`${label} is invalid`); return Math.round(n); };
export function normalizeItem(raw) {
  const id = clean(raw.id, 24).toUpperCase(), consignor = clean(raw.consignor, 80), name = clean(raw.name, 120);
  if (!id || !consignor || !name) throw new Error('Item identity is required');
  const salePrice = number(raw.salePrice, 'Sale price', 100, 100000000), commissionRate = number(raw.commissionRate, 'Commission rate', 0, 80);
  const dueDate = clean(raw.dueDate, 10); if (!/^\d{4}-\d{2}-\d{2}$/.test(dueDate)) throw new Error('Due date is invalid');
  const status = ['stocked','sold','settled'].includes(raw.status) ? raw.status : 'stocked';
  return { id, consignor, name, salePrice, commissionRate, dueDate, status };
}
export function amounts(item) { const fee = Math.round(item.salePrice * item.commissionRate / 100); return { fee, payout: item.salePrice - fee }; }
export function analyzeItem(item, today = '2026-08-16') {
  const { fee, payout } = amounts(item); const days = Math.ceil((new Date(item.dueDate + 'T00:00:00Z') - new Date(today + 'T00:00:00Z')) / 86400000);
  let risk = 'stock'; if (item.status === 'settled') risk = 'done'; else if (item.status === 'sold') risk = days < 0 ? 'overdue' : days <= 3 ? 'due-soon' : 'open';
  const rank = { overdue:0,'due-soon':1,open:2,stock:3,done:4 }[risk]; return { item, fee, payout, days, risk, rank };
}
export function dashboard(items, today) {
  const analyses = items.map(i => analyzeItem(i, today)).sort((a,b) => a.rank-b.rank || a.days-b.days || b.payout-a.payout);
  const unpaid = analyses.filter(a => ['overdue','due-soon','open'].includes(a.risk));
  return { items: items.length, sold: items.filter(i=>i.status!=='stocked').length, unpaid: unpaid.length, payoutDue: unpaid.reduce((s,a)=>s+a.payout,0), fees: items.filter(i=>i.status!=='stocked').reduce((s,i)=>s+amounts(i).fee,0), analyses };
}
export function addItem(items, raw) { const item = normalizeItem(raw); if (items.some(i=>i.id===item.id)) throw new Error('Item ID already exists'); return [...items,item]; }
export function sellItem(items, id) { if (!items.some(i=>i.id===id)) throw new Error('Item not found'); return items.map(i=>i.id===id && i.status==='stocked'?{...i,status:'sold'}:i); }
export function settleItem(items, id) { if (!items.some(i=>i.id===id && i.status==='sold')) throw new Error('Only sold items can be settled'); return items.map(i=>i.id===id?{...i,status:'settled'}:i); }
