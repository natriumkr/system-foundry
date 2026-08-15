export const STATUSES = ['open', 'completed', 'void'];

const clean = (value, max = 60) => String(value ?? '').trim().replace(/[<>]/g, '').slice(0, max);
const number = (value, label, min = 0, max = 100000000) => {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < min || parsed > max) throw new Error(`${label} is invalid`);
  return parsed;
};
const date = (value, label) => {
  const text = clean(value, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text) || Number.isNaN(Date.parse(`${text}T00:00:00Z`))) throw new Error(`${label} is invalid`);
  return text;
};

export function normalizeCredit(raw) {
  const reference = clean(raw.reference, 24).toUpperCase();
  const learner = clean(raw.learner, 40);
  const course = clean(raw.course, 50);
  if (!reference || !learner || !course) throw new Error('Identity is required');
  const issuedDate = date(raw.issuedDate, 'Issue date');
  const expiryDate = date(raw.expiryDate, 'Expiry date');
  if (expiryDate < issuedDate) throw new Error('Expiry must follow issue date');
  const sessions = number(raw.sessions, 'Sessions', 1, 100);
  const usedSessions = number(raw.usedSessions ?? 0, 'Used sessions', 0, sessions);
  const sessionValueKrw = number(raw.sessionValueKrw, 'Session value', 0, 10000000);
  const status = STATUSES.includes(raw.status) ? raw.status : 'open';
  return { reference, learner, course, issuedDate, expiryDate, sessions, usedSessions, sessionValueKrw, status };
}

export function remainingSessions(credit) {
  return credit.status === 'open' ? Math.max(0, credit.sessions - credit.usedSessions) : 0;
}

export function liability(credit) {
  return remainingSessions(credit) * credit.sessionValueKrw;
}

export function daysUntil(expiryDate, today = '2026-08-15') {
  return Math.ceil((Date.parse(`${expiryDate}T00:00:00Z`) - Date.parse(`${today}T00:00:00Z`)) / 86400000);
}

export function analyze(credit, today = '2026-08-15') {
  const remaining = remainingSessions(credit);
  const days = daysUntil(credit.expiryDate, today);
  let risk = 'closed';
  let rank = 5;
  if (credit.status === 'open' && remaining > 0) {
    if (days < 0) { risk = 'overdue'; rank = 0; }
    else if (days <= 7) { risk = 'urgent'; rank = 1; }
    else if (days <= 21) { risk = 'watch'; rank = 2; }
    else { risk = 'ready'; rank = 3; }
  }
  return { credit, remaining, days, risk, rank, liability: liability(credit) };
}

export function dashboard(credits, today = '2026-08-15') {
  const analyses = credits.map((item) => analyze(item, today)).sort((a, b) => a.rank - b.rank || a.days - b.days || b.liability - a.liability);
  return {
    openCredits: analyses.filter((item) => item.credit.status === 'open' && item.remaining > 0).length,
    sessions: analyses.reduce((sum, item) => sum + item.remaining, 0),
    liability: analyses.reduce((sum, item) => sum + item.liability, 0),
    dueSoon: analyses.filter((item) => ['overdue', 'urgent', 'watch'].includes(item.risk)).length,
    analyses,
  };
}

export function addCredit(credits, raw) {
  const credit = normalizeCredit(raw);
  if (credits.some((item) => item.reference.toUpperCase() === credit.reference)) throw new Error('Reference already exists');
  return [...credits, credit];
}

export function redeem(credits, reference, count = 1) {
  const amount = number(count, 'Redemption', 1, 100);
  return credits.map((credit) => {
    if (credit.reference !== reference) return credit;
    if (credit.status !== 'open' || remainingSessions(credit) < amount) throw new Error('Not enough sessions');
    const usedSessions = credit.usedSessions + amount;
    return { ...credit, usedSessions, status: usedSessions === credit.sessions ? 'completed' : 'open' };
  });
}
