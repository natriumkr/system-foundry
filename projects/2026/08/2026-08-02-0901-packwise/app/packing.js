export const CATEGORIES = ["documents", "clothes", "toiletries", "electronics", "accessories", "other"];

export function validateAllowance(value) {
  const kg = Number(value);
  if (!Number.isFinite(kg) || kg <= 0 || kg > 100) {
    throw new Error("Allowance must be between 0 and 100 kg");
  }
  return kg;
}

export function normalizeItem(raw) {
  const name = String(raw.name ?? "").trim();
  const category = String(raw.category ?? "other");
  const quantity = Number(raw.quantity);
  const unitGrams = Number(raw.unitGrams);

  if (name.length < 1 || name.length > 60) throw new Error("Item name must be 1-60 characters");
  if (!CATEGORIES.includes(category)) throw new Error("Unknown category");
  if (!Number.isInteger(quantity) || quantity < 1 || quantity > 99) {
    throw new Error("Quantity must be an integer from 1 to 99");
  }
  if (!Number.isFinite(unitGrams) || unitGrams < 0 || unitGrams > 50000) {
    throw new Error("Unit weight must be between 0 and 50,000 g");
  }

  return {
    id: String(raw.id || crypto.randomUUID()),
    name,
    category,
    quantity,
    unitGrams,
    packed: Boolean(raw.packed),
  };
}

export function calculateSummary(items, allowanceKg) {
  const allowance = validateAllowance(allowanceKg);
  const safeItems = items.map(normalizeItem);
  const units = safeItems.reduce((sum, item) => sum + item.quantity, 0);
  const packedUnits = safeItems.reduce((sum, item) => sum + (item.packed ? item.quantity : 0), 0);
  const totalGrams = safeItems.reduce((sum, item) => sum + item.quantity * item.unitGrams, 0);
  const packedGrams = safeItems.reduce(
    (sum, item) => sum + (item.packed ? item.quantity * item.unitGrams : 0),
    0,
  );
  const allowanceGrams = allowance * 1000;
  const remainingGrams = allowanceGrams - totalGrams;
  const loadPct = allowanceGrams === 0 ? 0 : (totalGrams / allowanceGrams) * 100;
  const progressPct = units === 0 ? 0 : (packedUnits / units) * 100;
  const status = remainingGrams < 0 ? "over" : loadPct >= 85 ? "near" : "safe";

  return {
    units,
    packedUnits,
    totalGrams,
    packedGrams,
    allowanceGrams,
    remainingGrams,
    loadPct,
    progressPct,
    status,
  };
}

export function serializePlan(plan) {
  const allowanceKg = validateAllowance(plan.allowanceKg);
  const tripName = String(plan.tripName ?? "").trim().slice(0, 80) || "My trip";
  const items = plan.items.map(normalizeItem);
  return JSON.stringify({ version: 1, tripName, allowanceKg, items }, null, 2);
}

export function parsePlan(json) {
  const data = JSON.parse(json);
  if (data?.version !== 1 || !Array.isArray(data.items)) throw new Error("Unsupported backup format");
  return {
    tripName: String(data.tripName ?? "").trim().slice(0, 80) || "My trip",
    allowanceKg: validateAllowance(data.allowanceKg),
    items: data.items.map(normalizeItem),
  };
}
