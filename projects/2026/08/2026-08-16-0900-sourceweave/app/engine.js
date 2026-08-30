export const SOURCE_TYPES = ['paper', 'official', 'book', 'news', 'web'];

const clean = (value, max = 160) => String(value ?? '').trim().replace(/[<>"'&]/g, '').slice(0, max);
const integer = (value, label, min, max) => {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed < min || parsed > max) throw new Error(`${label} is invalid`);
  return parsed;
};

export function normalizeSource(raw) {
  const id = clean(raw.id, 24).toUpperCase();
  const title = clean(raw.title, 120);
  const url = clean(raw.url, 300);
  const type = clean(raw.type, 12).toLowerCase();
  if (!id || !title || !SOURCE_TYPES.includes(type)) throw new Error('Source identity is invalid');
  if (!/^https:\/\/[a-z0-9.-]+(?:\/[^\s]*)?$/i.test(url)) throw new Error('Use a valid HTTPS URL');
  const credibility = integer(raw.credibility, 'Credibility', 1, 5);
  return { id, title, url, type, credibility };
}

export function normalizeClaim(raw) {
  const id = clean(raw.id, 24).toUpperCase();
  const text = clean(raw.text, 240);
  const importance = integer(raw.importance, 'Importance', 1, 5);
  const sourceIds = Array.isArray(raw.sourceIds) ? [...new Set(raw.sourceIds.map((item) => clean(item, 24).toUpperCase()).filter(Boolean))] : [];
  if (!id || !text) throw new Error('Claim is required');
  return { id, text, importance, sourceIds };
}

export function analyzeClaim(claim, sources) {
  const linked = claim.sourceIds.map((id) => sources.find((source) => source.id === id)).filter(Boolean);
  const independent = new Set(linked.map((source) => new URL(source.url).hostname.replace(/^www\./, ''))).size;
  const average = linked.length ? linked.reduce((sum, source) => sum + source.credibility, 0) / linked.length : 0;
  let status = 'gap';
  if (linked.length >= 2 && independent >= 2 && average >= 4) status = 'strong';
  else if (linked.length >= 1) status = 'supported';
  const rank = status === 'gap' ? 0 : status === 'supported' ? 1 : 2;
  const priority = claim.importance * 10 + (status === 'gap' ? 20 : status === 'supported' ? 10 : 0);
  return { claim, linked, independent, average: Math.round(average * 10) / 10, status, rank, priority };
}

export function dashboard(claims, sources) {
  const analyses = claims.map((claim) => analyzeClaim(claim, sources)).sort((a, b) => a.rank - b.rank || b.priority - a.priority || a.claim.id.localeCompare(b.claim.id));
  return {
    claims: claims.length,
    sources: sources.length,
    supported: analyses.filter((item) => item.status !== 'gap').length,
    strong: analyses.filter((item) => item.status === 'strong').length,
    gaps: analyses.filter((item) => item.status === 'gap').length,
    analyses,
  };
}

export function addSource(sources, raw) {
  const source = normalizeSource(raw);
  if (sources.some((item) => item.id.toUpperCase() === source.id)) throw new Error('Source ID already exists');
  return [...sources, source];
}

export function addClaim(claims, raw) {
  const claim = normalizeClaim(raw);
  if (claims.some((item) => item.id.toUpperCase() === claim.id)) throw new Error('Claim ID already exists');
  return [...claims, claim];
}

export function linkSource(claims, claimId, sourceId, sources) {
  if (!sources.some((source) => source.id === sourceId)) throw new Error('Source not found');
  return claims.map((claim) => claim.id === claimId ? { ...claim, sourceIds: [...new Set([...claim.sourceIds, sourceId])] } : claim);
}
