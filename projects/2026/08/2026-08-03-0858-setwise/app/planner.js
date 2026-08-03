(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.SetWisePlanner = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  class ValidationError extends Error {}

  function cleanText(value, label, maxLength) {
    const cleaned = String(value || "").trim().replace(/\s+/g, " ");
    if (!cleaned) throw new ValidationError(`${label}을(를) 입력하세요.`);
    if (cleaned.length > maxLength) throw new ValidationError(`${label}은(는) ${maxLength}자 이하여야 합니다.`);
    return cleaned;
  }

  function isoDate(value, label, optional = false) {
    if (!value && optional) return "";
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(value || "")) || Number.isNaN(Date.parse(`${value}T00:00:00Z`))) {
      throw new ValidationError(`${label} 날짜를 확인하세요.`);
    }
    return value;
  }

  function normalizePiece(input) {
    const confidence = Number(input.confidence);
    const minutes = Number(input.minutes);
    if (!Number.isInteger(confidence) || confidence < 1 || confidence > 5) {
      throw new ValidationError("자신감은 1부터 5 사이여야 합니다.");
    }
    if (!Number.isInteger(minutes) || minutes < 5 || minutes > 120) {
      throw new ValidationError("연습 시간은 5분부터 120분 사이여야 합니다.");
    }
    return {
      id: cleanText(input.id || `piece-${Date.now()}`, "ID", 80),
      title: cleanText(input.title, "곡명", 60),
      section: cleanText(input.section, "집중 구간", 60),
      confidence,
      minutes,
      lastPracticed: isoDate(input.lastPracticed, "최근 연습일", true),
      performanceDate: isoDate(input.performanceDate, "공연일", true),
    };
  }

  function parseDay(value) {
    return new Date(`${value}T00:00:00Z`);
  }

  function daysBetween(from, to) {
    return Math.round((parseDay(to) - parseDay(from)) / 86400000);
  }

  function priorityScore(piece, today) {
    const item = normalizePiece(piece);
    const confidenceNeed = (6 - item.confidence) * 18;
    const gap = item.lastPracticed ? Math.max(0, daysBetween(item.lastPracticed, today)) : 21;
    const recencyNeed = Math.min(gap, 30) * 2;
    let deadlineNeed = 0;
    if (item.performanceDate) {
      const remaining = daysBetween(today, item.performanceDate);
      if (remaining <= 0) deadlineNeed = 60;
      else if (remaining <= 7) deadlineNeed = 48 - remaining * 2;
      else if (remaining <= 30) deadlineNeed = 30 - remaining;
    }
    return Math.round(confidenceNeed + recencyNeed + deadlineNeed);
  }

  function buildQueue(pieces, availableMinutes, today) {
    const budget = Number(availableMinutes);
    if (!Number.isInteger(budget) || budget < 5 || budget > 240) {
      throw new ValidationError("오늘 연습 가능 시간은 5분부터 240분 사이여야 합니다.");
    }
    isoDate(today, "기준일");
    const ranked = pieces.map(normalizePiece)
      .map(piece => ({ ...piece, score: priorityScore(piece, today) }))
      .sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));
    const queue = [];
    let remaining = budget;
    for (const piece of ranked) {
      if (remaining < 5) break;
      const plannedMinutes = Math.min(piece.minutes, remaining);
      queue.push({ ...piece, plannedMinutes });
      remaining -= plannedMinutes;
    }
    return { queue, plannedMinutes: budget - remaining, remainingMinutes: remaining };
  }

  function completePractice(pieces, history, input) {
    const confidence = Number(input.confidence);
    const actualMinutes = Number(input.actualMinutes);
    if (!Number.isInteger(confidence) || confidence < 1 || confidence > 5) throw new ValidationError("완료 자신감을 확인하세요.");
    if (!Number.isInteger(actualMinutes) || actualMinutes < 1 || actualMinutes > 240) throw new ValidationError("실제 연습 시간을 확인하세요.");
    const practicedOn = isoDate(input.practicedOn, "연습일");
    const index = pieces.findIndex(piece => piece.id === input.pieceId);
    if (index < 0) throw new ValidationError("곡을 찾을 수 없습니다.");
    const nextPieces = pieces.map((piece, i) => i === index ? { ...piece, confidence, lastPracticed: practicedOn } : piece);
    const entry = {
      id: `session-${input.pieceId}-${practicedOn}-${history.length + 1}`,
      pieceId: input.pieceId,
      title: pieces[index].title,
      actualMinutes,
      confidence,
      practicedOn,
    };
    return { pieces: nextPieces, history: [entry, ...history].slice(0, 50) };
  }

  function summary(pieces, history, today) {
    const weekStart = new Date(`${today}T00:00:00Z`);
    weekStart.setUTCDate(weekStart.getUTCDate() - 6);
    const weekStartIso = weekStart.toISOString().slice(0, 10);
    const dueSoon = pieces.filter(piece => piece.performanceDate && daysBetween(today, piece.performanceDate) >= 0 && daysBetween(today, piece.performanceDate) <= 14).length;
    const weekMinutes = history.filter(entry => entry.practicedOn >= weekStartIso && entry.practicedOn <= today)
      .reduce((total, entry) => total + Number(entry.actualMinutes || 0), 0);
    return { repertoire: pieces.length, dueSoon, weekMinutes };
  }

  return { ValidationError, normalizePiece, priorityScore, buildQueue, completePractice, summary, daysBetween };
});
