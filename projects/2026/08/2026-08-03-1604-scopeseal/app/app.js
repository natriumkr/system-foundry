const Engine = window.ScopeSeal;
const STORAGE_KEY = "scopeseal.v1";
const today = new Date().toISOString().slice(0, 10);

const defaults = {
  contract: { projectName: "Orbit Brand Refresh", clientAlias: "O Studio", includedRounds: 2, hourlyRate: 60000 },
  requests: [
    { id: "req-1", title: "메인 비주얼 교체", detail: "첫 화면 제품 이미지와 카피 조정", inScope: true, estimatedHours: 2, status: "done", createdOn: "2026-07-30" },
    { id: "req-2", title: "모바일 여백 수정", detail: "상세 페이지 모바일 간격 정리", inScope: true, estimatedHours: 1, status: "approved", createdOn: "2026-08-01" },
    { id: "req-3", title: "추가 랜딩 페이지", detail: "신제품 캠페인용 신규 페이지 제작", inScope: false, estimatedHours: 6, status: "quoted", createdOn: "2026-08-02" },
    { id: "req-4", title: "SNS 배너 2종", detail: "정사각형과 세로형 프로모션 배너", inScope: false, estimatedHours: 2, status: "new", createdOn: "2026-08-03" },
  ],
};

let state = load();

function load() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (parsed && parsed.contract && Array.isArray(parsed.requests)) return parsed;
  } catch (_) {}
  return structuredClone(defaults);
}

function save() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function money(value) { return `₩${Number(value).toLocaleString("ko-KR")}`; }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, char => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", "'":"&#39;", '"':"&quot;" }[char])); }
const statusLabels = { new: "검토 전", quoted: "견적 전달", approved: "승인", done: "완료" };

function render() {
  const result = Engine.evaluateRequests(state.contract, state.requests);
  const { summary } = result;
  document.querySelector("#project-name").textContent = result.contract.projectName;
  document.querySelector("#client-alias").textContent = result.contract.clientAlias;
  document.querySelector("#open-count").textContent = summary.openRequests;
  document.querySelector("#remaining-count").textContent = `${summary.remainingRounds}회`;
  document.querySelector("#billable-total").textContent = money(summary.billableTotal);
  document.querySelector("#approval-count").textContent = `${summary.awaitingApproval}건 승인 대기`;
  document.querySelector("#contract-summary").textContent = `포함 ${result.contract.includedRounds}회 · 시간당 ${money(result.contract.hourlyRate)}`;
  document.querySelector("#request-date").value = today;
  document.querySelector("#request-list").innerHTML = result.requests.slice().reverse().map(request => `
    <article class="request-card ${request.billable ? "billable" : "included"}">
      <div class="request-kind"><span>${request.billable ? "추가 청구" : "계약 포함"}</span><small>${request.reason}</small></div>
      <div class="request-main"><div class="request-meta"><span>${request.createdOn}</span><span>${request.estimatedHours}시간 예상</span></div>
        <h3>${escapeHtml(request.title)}</h3><p>${escapeHtml(request.detail || "상세 내용 없음")}</p></div>
      <div class="request-price"><span>예상 청구</span><b>${request.billable ? money(request.charge) : "포함"}</b></div>
      <form class="status-form" data-status-form="${request.id}"><select name="status">${Object.entries(statusLabels).map(([value,label]) => `<option value="${value}" ${request.status === value ? "selected" : ""}>${label}</option>`).join("")}</select><button>저장</button></form>
    </article>`).join("");
  document.querySelector("#included-progress").style.width = `${Math.min(100, (summary.includedUsed / Math.max(1, result.contract.includedRounds)) * 100)}%`;
  document.querySelector("#included-copy").textContent = `${summary.includedUsed} / ${result.contract.includedRounds}회 사용`;
}

document.querySelector("#request-form").addEventListener("submit", event => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(event.currentTarget));
  try {
    const request = Engine.normalizeRequest({ ...values, id: `req-${Date.now()}`, inScope: values.inScope === "true", status: "new" });
    state.requests.push(request);
    save();
    event.currentTarget.reset();
    document.querySelector("#notice").textContent = "수정 요청을 등록했습니다.";
    render();
  } catch (error) { document.querySelector("#form-message").textContent = error.message; }
});

document.querySelector("#request-list").addEventListener("submit", event => {
  const form = event.target.closest("[data-status-form]");
  if (!form) return;
  event.preventDefault();
  try {
    state.requests = Engine.updateStatus(state.requests, form.dataset.statusForm, new FormData(form).get("status"));
    save();
    document.querySelector("#notice").textContent = "처리 상태를 갱신했습니다.";
    render();
  } catch (error) { document.querySelector("#notice").textContent = error.message; }
});

document.querySelector("#contract-form").addEventListener("submit", event => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(event.currentTarget));
  try {
    state.contract = Engine.normalizeContract(values);
    save();
    document.querySelector("#contract-message").textContent = "계약 기준을 저장했습니다.";
    render();
  } catch (error) { document.querySelector("#contract-message").textContent = error.message; }
});

document.querySelector("#settings").addEventListener("click", () => {
  const dialog = document.querySelector("#contract-dialog");
  const form = document.querySelector("#contract-form");
  Object.entries(state.contract).forEach(([key,value]) => { if (form.elements[key]) form.elements[key].value = value; });
  dialog.showModal();
});
document.querySelector("#close-dialog").addEventListener("click", () => document.querySelector("#contract-dialog").close());
document.querySelector("#reset").addEventListener("click", () => { state = structuredClone(defaults); save(); document.querySelector("#notice").textContent = "샘플 데이터를 복원했습니다."; render(); });

render();
