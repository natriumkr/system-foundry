const Planner = window.SetWisePlanner;
const STORAGE_KEY = "setwise.v1";
const today = new Date().toISOString().slice(0, 10);

function offsetDate(days) {
  const value = new Date(`${today}T00:00:00Z`);
  value.setUTCDate(value.getUTCDate() + days);
  return value.toISOString().slice(0, 10);
}

const defaults = {
  pieces: [
    { id: "bach-prelude", title: "Bach Prelude", section: "16-24마디 연결", confidence: 2, minutes: 15, lastPracticed: offsetDate(-5), performanceDate: offsetDate(12) },
    { id: "jazz-etude", title: "Jazz Etude No. 3", section: "브리지 리듬", confidence: 3, minutes: 12, lastPracticed: offsetDate(-3), performanceDate: offsetDate(21) },
    { id: "open-ending", title: "Open Ending", section: "후렴 전환", confidence: 4, minutes: 10, lastPracticed: offsetDate(-1), performanceDate: offsetDate(6) },
    { id: "scale-routine", title: "Scale Routine", section: "E major 아르페지오", confidence: 2, minutes: 8, lastPracticed: offsetDate(-7), performanceDate: "" },
  ],
  history: [
    { id: "sample-1", pieceId: "open-ending", title: "Open Ending", actualMinutes: 14, confidence: 4, practicedOn: offsetDate(-1) },
    { id: "sample-2", pieceId: "jazz-etude", title: "Jazz Etude No. 3", actualMinutes: 18, confidence: 3, practicedOn: offsetDate(-3) },
  ],
  availableMinutes: 35,
};

let state = load();
let plan = Planner.buildQueue(state.pieces, state.availableMinutes, today);

function load() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (parsed && Array.isArray(parsed.pieces) && Array.isArray(parsed.history)) return parsed;
  } catch (_) {}
  return structuredClone(defaults);
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function riskLabel(score) {
  if (score >= 125) return ["지금 먼저", "hot"];
  if (score >= 95) return ["오늘 권장", "warm"];
  return ["여유 있음", "cool"];
}

function render() {
  const summary = Planner.summary(state.pieces, state.history, today);
  document.querySelector("#today").textContent = today.replaceAll("-", ".");
  document.querySelector("#repertoire-count").textContent = summary.repertoire;
  document.querySelector("#due-count").textContent = summary.dueSoon;
  document.querySelector("#week-minutes").textContent = `${summary.weekMinutes}분`;
  document.querySelector("#minutes").value = state.availableMinutes;
  document.querySelector("#minutes-label").textContent = `${state.availableMinutes}분`;
  document.querySelector("#plan-total").textContent = `${plan.plannedMinutes}분 계획`;
  document.querySelector("#queue").innerHTML = plan.queue.map((item, index) => {
    const [label, tone] = riskLabel(item.score);
    const performance = item.performanceDate ? `공연 D-${Math.max(0, Planner.daysBetween(today, item.performanceDate))}` : "공연일 없음";
    return `<article class="queue-card">
      <div class="rank">0${index + 1}</div>
      <div class="piece-main"><div class="piece-top"><span class="priority ${tone}">${label}</span><span>${performance}</span></div>
      <h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.section)}</p>
      <div class="confidence"><span>현재 자신감</span><div>${[1,2,3,4,5].map(n => `<i class="${n <= item.confidence ? "on" : ""}"></i>`).join("")}</div></div></div>
      <div class="session"><b>${item.plannedMinutes}</b><span>MIN</span><label>완료 후 자신감<select data-confidence="${item.id}">${[1,2,3,4,5].map(n => `<option value="${n}" ${n === item.confidence ? "selected" : ""}>${n}</option>`).join("")}</select></label>
      <button data-complete="${item.id}" data-minutes="${item.plannedMinutes}">연습 완료</button></div>
    </article>`;
  }).join("") || `<div class="empty">레퍼토리를 추가해 오늘의 큐를 만들어 보세요.</div>`;
  document.querySelector("#history").innerHTML = state.history.slice(0, 4).map(entry => `<li><span class="history-dot"></span><div><b>${escapeHtml(entry.title)}</b><small>${entry.practicedOn} · 자신감 ${entry.confidence}/5</small></div><strong>${entry.actualMinutes}분</strong></li>`).join("") || `<li class="empty">아직 완료한 연습이 없습니다.</li>`;
}

function rebuild() {
  plan = Planner.buildQueue(state.pieces, state.availableMinutes, today);
  save();
  render();
}

document.querySelector("#minutes").addEventListener("input", event => {
  state.availableMinutes = Number(event.target.value);
  rebuild();
});

document.querySelector("#piece-form").addEventListener("submit", event => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  try {
    const piece = Planner.normalizePiece({ ...data, id: `piece-${Date.now()}`, lastPracticed: "" });
    state.pieces.push(piece);
    event.currentTarget.reset();
    document.querySelector("#form-message").textContent = "레퍼토리에 추가했습니다.";
    rebuild();
  } catch (error) {
    document.querySelector("#form-message").textContent = error.message;
  }
});

document.querySelector("#queue").addEventListener("click", event => {
  const button = event.target.closest("[data-complete]");
  if (!button) return;
  const pieceId = button.dataset.complete;
  const confidence = Number(document.querySelector(`[data-confidence="${pieceId}"]`).value);
  try {
    const result = Planner.completePractice(state.pieces, state.history, {
      pieceId, confidence, actualMinutes: Number(button.dataset.minutes), practicedOn: today,
    });
    state.pieces = result.pieces;
    state.history = result.history;
    document.querySelector("#notice").textContent = "연습 기록을 저장했습니다.";
    rebuild();
  } catch (error) {
    document.querySelector("#notice").textContent = error.message;
  }
});

document.querySelector("#reset").addEventListener("click", () => {
  state = structuredClone(defaults);
  document.querySelector("#notice").textContent = "샘플 데이터를 복원했습니다.";
  rebuild();
});

rebuild();
