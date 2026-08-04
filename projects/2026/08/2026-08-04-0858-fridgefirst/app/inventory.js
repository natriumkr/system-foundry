(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.FridgeFirst = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  class ValidationError extends Error {}
  const categories = new Set(["produce", "dairy", "protein", "meal", "other"]);
  const outcomes = new Set(["consumed", "wasted"]);

  function cleanText(value, label, max) {
    const text = String(value ?? "").trim().replace(/\s+/g, " ");
    if (!text || text.length > max) throw new ValidationError(`${label}은 1~${max}자로 입력하세요.`);
    return text;
  }

  function asNumber(value, label, min, max) {
    const number = Number(value);
    if (!Number.isFinite(number) || number < min || number > max) throw new ValidationError(`${label} 범위를 확인하세요.`);
    return Math.round(number * 100) / 100;
  }

  function normalizeItem(input) {
    const category = String(input.category ?? "");
    if (!categories.has(category)) throw new ValidationError("식품 분류를 확인하세요.");
    const expiresOn = String(input.expiresOn ?? "");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(expiresOn) || Number.isNaN(Date.parse(`${expiresOn}T00:00:00Z`))) throw new ValidationError("유효한 소비기한을 입력하세요.");
    return {
      id: cleanText(input.id, "항목 ID", 80),
      name: cleanText(input.name, "식품명", 60),
      category,
      quantity: asNumber(input.quantity, "수량", 0.1, 999),
      unit: cleanText(input.unit, "단위", 12),
      value: Math.round(asNumber(input.value, "구매가", 0, 10000000)),
      expiresOn,
      addedOn: String(input.addedOn || expiresOn),
    };
  }

  function daysBetween(today, date) {
    return Math.round((Date.parse(`${date}T00:00:00Z`) - Date.parse(`${today}T00:00:00Z`)) / 86400000);
  }

  function classify(days) {
    if (days < 0) return { key: "expired", label: "기한 지남", rank: 0 };
    if (days === 0) return { key: "today", label: "오늘까지", rank: 1 };
    if (days <= 3) return { key: "soon", label: `${days}일 남음`, rank: 2 };
    return { key: "later", label: `${days}일 남음`, rank: 3 };
  }

  function buildQueue(items, today) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(today)) throw new ValidationError("기준일을 확인하세요.");
    const queue = items.map(normalizeItem).map(item => {
      const daysLeft = daysBetween(today, item.expiresOn);
      return { ...item, daysLeft, urgency: classify(daysLeft) };
    }).sort((a, b) => a.urgency.rank - b.urgency.rank || a.daysLeft - b.daysLeft || b.value - a.value || a.name.localeCompare(b.name));
    return {
      items: queue,
      summary: {
        totalItems: queue.length,
        urgentItems: queue.filter(item => item.daysLeft <= 3).length,
        valueAtRisk: queue.filter(item => item.daysLeft <= 3).reduce((sum, item) => sum + item.value, 0),
      },
    };
  }

  function recordOutcome(items, history, id, outcome, recordedOn) {
    if (!outcomes.has(outcome)) throw new ValidationError("처리 결과를 확인하세요.");
    const index = items.findIndex(item => item.id === id);
    if (index < 0) throw new ValidationError("처리할 식품을 찾을 수 없습니다.");
    const item = normalizeItem(items[index]);
    const nextItems = items.filter((_, itemIndex) => itemIndex !== index);
    const nextHistory = [...history, { id: `log-${id}-${recordedOn}`, itemId: id, name: item.name, value: item.value, outcome, recordedOn }];
    return { items: nextItems, history: nextHistory };
  }

  function summarizeHistory(history) {
    return history.reduce((summary, entry) => {
      if (entry.outcome === "consumed") summary.savedValue += Number(entry.value) || 0;
      if (entry.outcome === "wasted") summary.wastedValue += Number(entry.value) || 0;
      summary.actions += 1;
      return summary;
    }, { savedValue: 0, wastedValue: 0, actions: 0 });
  }

  return { ValidationError, normalizeItem, buildQueue, recordOutcome, summarizeHistory };
});
