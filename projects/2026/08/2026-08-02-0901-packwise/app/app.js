import { calculateSummary, normalizeItem, serializePlan } from "./packing.js";

const seedItems = [
  ["여권", "documents", 1, 50, true],
  ["티셔츠", "clothes", 4, 180, true],
  ["속옷", "clothes", 4, 70, true],
  ["청바지", "clothes", 1, 650, false],
  ["후드 집업", "clothes", 1, 650, false],
  ["세면 파우치", "toiletries", 1, 650, true],
  ["휴대폰 충전기", "electronics", 1, 180, false],
  ["보조배터리", "electronics", 1, 350, false],
  ["카메라", "electronics", 1, 720, false],
  ["운동화", "accessories", 1, 850, false],
  ["접이식 우산", "accessories", 1, 280, false],
].map(([name, category, quantity, unitGrams, packed], index) => ({
  id: `seed-${index}`,
  name,
  category,
  quantity,
  unitGrams,
  packed,
}));

const categoryLabels = {
  documents: "서류",
  clothes: "의류",
  toiletries: "세면",
  electronics: "전자기기",
  accessories: "소품",
  other: "기타",
};

const stored = localStorage.getItem("packwise-plan");
let state = stored ? JSON.parse(stored) : {
  tripName: "제주 4일 여행",
  allowanceKg: 10,
  items: seedItems,
};

const tripName = document.querySelector("#trip-name");
const allowance = document.querySelector("#allowance");
const list = document.querySelector("#packing-list");
const form = document.querySelector("#item-form");
const status = document.querySelector("#form-status");

tripName.value = state.tripName;
allowance.value = state.allowanceKg;

function kg(grams) {
  return `${(grams / 1000).toFixed(2)} kg`;
}

function persist() {
  localStorage.setItem("packwise-plan", JSON.stringify(state));
}

function render() {
  try {
    const summary = calculateSummary(state.items, state.allowanceKg);
    document.querySelector("#total-weight").textContent = kg(summary.totalGrams);
    document.querySelector("#remaining-weight").textContent = summary.remainingGrams >= 0
      ? `${kg(summary.remainingGrams)} 남음`
      : `${kg(Math.abs(summary.remainingGrams))} 초과`;
    document.querySelector("#packed-count").textContent = `${summary.packedUnits} / ${summary.units}`;
    document.querySelector("#progress-percent").textContent = `${Math.round(summary.progressPct)}%`;
    document.querySelector("#weight-bar").style.width = `${Math.min(summary.loadPct, 100)}%`;
    document.querySelector("#progress-bar").style.width = `${summary.progressPct}%`;
    document.querySelector("#weight-card").dataset.state = summary.status;
    document.querySelector("#weight-label").textContent = summary.status === "over"
      ? "허용 중량을 줄여야 합니다"
      : summary.status === "near" ? "허용 중량에 근접했습니다" : "아직 여유가 있습니다";

    list.replaceChildren(...state.items.map(itemRow));
    persist();
    status.textContent = "";
  } catch (error) {
    status.textContent = error.message;
  }
}

function itemRow(item) {
  const row = document.createElement("article");
  row.className = `item-row${item.packed ? " packed" : ""}`;
  row.innerHTML = `
    <button class="check" aria-label="포장 상태 변경">${item.packed ? "✓" : ""}</button>
    <div class="item-copy"><strong></strong><span></span></div>
    <span class="item-weight"></span>
    <button class="remove" aria-label="항목 삭제">×</button>`;
  row.querySelector("strong").textContent = item.name;
  row.querySelector(".item-copy span").textContent = `${categoryLabels[item.category]} · ${item.quantity}개`;
  row.querySelector(".item-weight").textContent = kg(item.quantity * item.unitGrams);
  row.querySelector(".check").addEventListener("click", () => {
    item.packed = !item.packed;
    render();
  });
  row.querySelector(".remove").addEventListener("click", () => {
    state.items = state.items.filter(candidate => candidate.id !== item.id);
    render();
  });
  return row;
}

tripName.addEventListener("input", () => {
  state.tripName = tripName.value.slice(0, 80);
  persist();
});

allowance.addEventListener("input", () => {
  state.allowanceKg = Number(allowance.value);
  render();
});

form.addEventListener("submit", event => {
  event.preventDefault();
  try {
    const data = Object.fromEntries(new FormData(form).entries());
    state.items.push(normalizeItem(data));
    form.reset();
    form.querySelector("[name=quantity]").value = "1";
    render();
  } catch (error) {
    status.textContent = error.message;
  }
});

document.querySelector("#export-plan").addEventListener("click", () => {
  const content = serializePlan(state);
  const blob = new Blob([content], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "packwise-plan.json";
  anchor.click();
  URL.revokeObjectURL(url);
});

document.querySelector("#reset-plan").addEventListener("click", () => {
  state = { tripName: "새 여행", allowanceKg: 10, items: [] };
  tripName.value = state.tripName;
  allowance.value = state.allowanceKg;
  render();
});

render();
