import { buildCsv, calculateEconomics } from "./calculator.js";

const form = document.querySelector("#calculator-form");
const status = document.querySelector("#status");
const exportButton = document.querySelector("#export-csv");
let latestResult = null;

const won = new Intl.NumberFormat("ko-KR", {
  style: "currency",
  currency: "KRW",
  maximumFractionDigits: 0,
});

function formatWon(value) {
  return value === null ? "계산 불가" : won.format(Math.round(value));
}

function formatPct(value) {
  return `${value.toFixed(1)}%`;
}

function collectInputs() {
  return Object.fromEntries(new FormData(form).entries());
}

function setText(id, value) {
  document.querySelector(`#${id}`).textContent = value;
}

function render() {
  try {
    latestResult = calculateEconomics(collectInputs());
    setText("unit-profit", formatWon(latestResult.unitProfit));
    setText("margin", formatPct(latestResult.marginPct));
    setText("monthly-profit", formatWon(latestResult.monthlyProfit));
    setText("break-even", formatWon(latestResult.breakEvenPrice));
    setText("target-price", formatWon(latestResult.targetPrice));
    setText("total-cost", formatWon(latestResult.totalUnitCost));
    setText("fee-cost", formatWon(latestResult.variableFees));
    setText("return-cost", formatWon(latestResult.returnExpectedCost));
    setText("fixed-cost", formatWon(latestResult.fixedCostPerOrder));

    const positive = latestResult.unitProfit >= 0;
    document.querySelector("#profit-card").dataset.state = positive ? "positive" : "negative";
    status.textContent = latestResult.targetPrice === null
      ? "목표 마진과 비율 비용의 합이 100% 이상입니다. 값을 낮춰주세요."
      : "모든 금액은 주문 1건 기준이며 반품비는 기대값으로 반영됩니다.";
    status.dataset.error = latestResult.targetPrice === null ? "true" : "false";
    exportButton.disabled = false;
  } catch (error) {
    latestResult = null;
    status.textContent = `입력 확인: ${error.message}`;
    status.dataset.error = "true";
    exportButton.disabled = true;
  }
}

form.addEventListener("input", render);
form.addEventListener("submit", (event) => {
  event.preventDefault();
  render();
});

exportButton.addEventListener("click", () => {
  if (!latestResult) return;
  const blob = new Blob(["\uFEFF", buildCsv(latestResult)], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "marginmap-analysis.csv";
  anchor.click();
  URL.revokeObjectURL(url);
});

render();
