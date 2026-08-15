export const MATERIALS = ['PLA', 'PETG', 'ABS', 'TPU', 'ASA'];

const clean = (value, max = 50) => String(value ?? '').trim().replace(/[<>]/g, '').slice(0, max);
const number = (value, label, min = 0, max = 1000000) => {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < min || parsed > max) throw new Error(`${label} is invalid`);
  return parsed;
};

export function normalizeSpool(raw) {
  const id = clean(raw.id, 24).toUpperCase();
  const color = clean(raw.color, 30);
  const material = clean(raw.material, 8).toUpperCase();
  if (!id || !color || !MATERIALS.includes(material)) throw new Error('Spool identity is invalid');
  const tareG = number(raw.tareG, 'Tare', 1, 2000);
  const grossG = number(raw.grossG, 'Gross', tareG, 10000);
  const purchaseG = number(raw.purchaseG, 'Purchase weight', 1, 10000);
  const priceKrw = number(raw.priceKrw, 'Price', 0, 1000000);
  return { id, color, material, tareG, grossG, purchaseG, priceKrw, status: raw.status === 'archived' ? 'archived' : 'active' };
}

export function remainingG(spool) {
  return Math.max(0, Math.round((spool.grossG - spool.tareG) * 10) / 10);
}

export function remainingValue(spool) {
  return Math.round((remainingG(spool) / spool.purchaseG) * spool.priceKrw);
}

export function normalizeJob(raw) {
  const name = clean(raw.name, 50);
  const material = clean(raw.material, 8).toUpperCase();
  if (!name || !MATERIALS.includes(material)) throw new Error('Job is invalid');
  const requiredG = number(raw.requiredG, 'Required weight', 1, 10000);
  const safetyPct = number(raw.safetyPct, 'Safety margin', 0, 100);
  return { name, material, requiredG, safetyPct };
}

export function requiredWithMargin(job) {
  return Math.ceil(job.requiredG * (1 + job.safetyPct / 100));
}

export function analyze(spool, job) {
  const remaining = remainingG(spool);
  const needed = requiredWithMargin(job);
  const compatible = spool.status === 'active' && spool.material === job.material;
  return {
    spool,
    remaining,
    needed,
    fits: compatible && remaining >= needed,
    shortage: compatible ? Math.max(0, needed - remaining) : null,
    runs: compatible ? Math.floor(remaining / needed) : 0,
  };
}

export function dashboard(spools, job) {
  const active = spools.filter((spool) => spool.status === 'active');
  const analyses = job ? active.map((spool) => analyze(spool, job)) : [];
  analyses.sort((a, b) => Number(b.fits) - Number(a.fits) || b.runs - a.runs || b.remaining - a.remaining);
  return {
    spools: active.length,
    grams: active.reduce((sum, spool) => sum + remainingG(spool), 0),
    value: active.reduce((sum, spool) => sum + remainingValue(spool), 0),
    matches: analyses.filter((item) => item.fits).length,
    analyses,
  };
}

export function addSpool(spools, raw) {
  const spool = normalizeSpool(raw);
  if (spools.some((item) => item.id.toUpperCase() === spool.id)) throw new Error('Spool code already exists');
  return [...spools, spool];
}

export function consume(spools, id, grams) {
  const used = number(grams, 'Consumption', 0.1, 10000);
  return spools.map((spool) => {
    if (spool.id !== id) return spool;
    if (remainingG(spool) < used) throw new Error('Not enough filament');
    return { ...spool, grossG: Math.round((spool.grossG - used) * 10) / 10 };
  });
}
