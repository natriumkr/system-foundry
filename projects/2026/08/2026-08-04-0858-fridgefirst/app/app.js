const Engine = window.FridgeFirst;
const STORAGE_KEY = "fridgefirst.v1";
const today = "2026-08-04";
const categoryLabels = { produce: "채소·과일", dairy: "유제품", protein: "단백질", meal: "간편식", other: "기타" };

const defaults = {
  items: [
    { id: "food-1", name: "샐러드 채소", category: "produce", quantity: 1, unit: "봉", value: 6500, expiresOn: "2026-08-04", addedOn: "2026-08-01" },
    { id: "food-2", name: "그릭 요거트", category: "dairy", quantity: 2, unit: "개", value: 4500, expiresOn: "2026-08-05", addedOn: "2026-08-01" },
    { id: "food-3", name: "부침용 두부", category: "protein", quantity: 1, unit: "모", value: 2800, expiresOn: "2026-08-06", addedOn: "2026-08-02" },
    { id: "food-4", name: "달걀", category: "protein", quantity: 10, unit: "알", value: 7200, expiresOn: "2026-08-11", addedOn: "2026-08-01" },
    { id: "food-5", name: "냉동 만두", category: "meal", quantity: 1, unit: "봉", value: 9800, expiresOn: "2026-09-01", addedOn: "2026-08-01" },
  ],
  history: [],
};

function load() {
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (data && Array.isArray(data.items) && Array.isArray(data.history)) return data;
  } catch (_) {}
  return structuredClone(defaults);
}

let state = load();
const money = value => `₩${Number(value).toLocaleString("ko-KR")}`;
const escapeHtml = value => String(value).replace(/[&<>'"]/g, char => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", "'":"&#39;", '"':"&quot;" }[char]));
function save() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }

function render() {
  const queue = Engine.buildQueue(state.items, today);
  const history = Engine.summarizeHistory(state.history);
  document.querySelector("#total-items").textContent = queue.summary.totalItems;
  document.querySelector("#urgent-items").textContent = queue.summary.urgentItems;
  document.querySelector("#risk-value").textContent = money(queue.summary.valueAtRisk);
  document.querySelector("#saved-value").textContent = money(history.savedValue);
  document.querySelector("#history-copy").textContent = history.actions ? `${history.actions}건 처리 · 낭비 ${money(history.wastedValue)}` : "아직 처리 기록이 없습니다";
  document.querySelector("#item-list").innerHTML = queue.items.map(item => `
    <article class="food-card ${item.urgency.key}" data-card="${item.id}">
      <div class="urgency"><span>${item.urgency.label}</span><small>${item.daysLeft < 0 ? "섭취하지 말고 상태를 확인하세요" : categoryLabels[item.category]}</small></div>
      <div class="food-copy"><div class="meta"><span>${item.expiresOn}</span><span>${item.quantity}${escapeHtml(item.unit)}</span></div><h3>${escapeHtml(item.name)}</h3><p>${item.daysLeft < 0 ? "기한이 지나 폐기 대상으로 분류되었습니다." : "먼저 소비하면 낭비를 줄일 수 있습니다."}</p></div>
      <div class="food-value"><span>구매가</span><b>${money(item.value)}</b></div>
      <div class="actions">${item.daysLeft < 0 ? "" : `<button data-action="consumed" data-id="${item.id}">사용 완료</button>`}<button class="ghost" data-action="wasted" data-id="${item.id}">폐기 기록</button></div>
    </article>`).join("");
  if (!queue.items.length) document.querySelector("#item-list").innerHTML = '<div class="empty">등록된 식품이 없습니다. 다음 장보기부터 기록해 보세요.</div>';
}

document.querySelector("#item-form").addEventListener("submit", event => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(event.currentTarget));
  try {
    const newItem = Engine.normalizeItem({ ...values, id: `food-${Date.now()}`, addedOn: today });
    state.items.push(newItem);
    save();
    event.currentTarget.reset();
    document.querySelector("#expiry-date").value = "2026-08-07";
    document.querySelector("#notice").textContent = "식품을 등록하고 소비 우선순위를 갱신했습니다.";
    document.querySelector("#form-message").textContent = "";
    render();
  } catch (error) { document.querySelector("#form-message").textContent = error.message; }
});

document.querySelector("#item-list").addEventListener("click", event => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  try {
    const result = Engine.recordOutcome(state.items, state.history, button.dataset.id, button.dataset.action, today);
    state = result;
    save();
    document.querySelector("#notice").textContent = button.dataset.action === "consumed" ? "사용 완료로 기록했습니다." : "폐기로 기록했습니다.";
    render();
  } catch (error) { document.querySelector("#notice").textContent = error.message; }
});

document.querySelector("#reset").addEventListener("click", () => {
  state = structuredClone(defaults); save(); document.querySelector("#notice").textContent = "샘플 데이터를 복원했습니다."; render();
});
document.querySelector("#expiry-date").value = "2026-08-07";
render();
