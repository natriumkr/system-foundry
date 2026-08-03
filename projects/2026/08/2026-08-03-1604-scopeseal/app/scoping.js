(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.ScopeSeal = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  class ValidationError extends Error {}
  const STATUSES = new Set(["new", "quoted", "approved", "done"]);

  function cleanText(value, label, maxLength, required = true) {
    const cleaned = String(value || "").trim().replace(/\s+/g, " ");
    if (required && !cleaned) throw new ValidationError(`${label}을(를) 입력하세요.`);
    if (cleaned.length > maxLength) throw new ValidationError(`${label}은(는) ${maxLength}자 이하여야 합니다.`);
    return cleaned;
  }

  function normalizeContract(input) {
    const includedRounds = Number(input.includedRounds);
    const hourlyRate = Number(input.hourlyRate);
    if (!Number.isInteger(includedRounds) || includedRounds < 0 || includedRounds > 20) {
      throw new ValidationError("포함 수정 횟수는 0회부터 20회 사이여야 합니다.");
    }
    if (!Number.isInteger(hourlyRate) || hourlyRate < 10000 || hourlyRate > 1000000) {
      throw new ValidationError("시간당 단가는 1만원부터 100만원 사이여야 합니다.");
    }
    return {
      projectName: cleanText(input.projectName, "프로젝트명", 60),
      clientAlias: cleanText(input.clientAlias, "고객 별칭", 40),
      includedRounds,
      hourlyRate,
    };
  }

  function normalizeRequest(input) {
    const estimatedHours = Number(input.estimatedHours);
    if (!Number.isFinite(estimatedHours) || estimatedHours < 0.5 || estimatedHours > 100 || Math.round(estimatedHours * 2) !== estimatedHours * 2) {
      throw new ValidationError("예상 작업시간은 0.5시간 단위로 0.5시간부터 100시간 사이여야 합니다.");
    }
    const status = input.status || "new";
    if (!STATUSES.has(status)) throw new ValidationError("올바른 처리 상태를 선택하세요.");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(input.createdOn || "") || Number.isNaN(Date.parse(`${input.createdOn}T00:00:00Z`))) {
      throw new ValidationError("요청일을 확인하세요.");
    }
    return {
      id: cleanText(input.id || `request-${Date.now()}`, "ID", 80),
      title: cleanText(input.title, "요청 제목", 70),
      detail: cleanText(input.detail, "요청 내용", 240, false),
      inScope: input.inScope === true || input.inScope === "true",
      estimatedHours,
      status,
      createdOn: input.createdOn,
    };
  }

  function evaluateRequests(contractInput, requestInputs) {
    const contract = normalizeContract(contractInput);
    let includedUsed = 0;
    const requests = requestInputs.map(normalizeRequest).map(request => {
      const hasAllowance = request.inScope && includedUsed < contract.includedRounds;
      if (hasAllowance) includedUsed += 1;
      const billable = !hasAllowance;
      return {
        ...request,
        allowanceNumber: hasAllowance ? includedUsed : null,
        billable,
        charge: billable ? Math.round(request.estimatedHours * contract.hourlyRate) : 0,
        reason: hasAllowance ? "계약 포함" : (request.inScope ? "포함 횟수 초과" : "계약 범위 밖"),
      };
    });
    const active = requests.filter(request => request.status !== "done");
    return {
      contract,
      requests,
      summary: {
        openRequests: active.length,
        includedUsed,
        remainingRounds: Math.max(0, contract.includedRounds - includedUsed),
        billableTotal: requests.filter(request => request.billable).reduce((sum, request) => sum + request.charge, 0),
        awaitingApproval: requests.filter(request => request.billable && ["new", "quoted"].includes(request.status)).length,
      },
    };
  }

  function updateStatus(requests, id, status) {
    if (!STATUSES.has(status)) throw new ValidationError("올바른 처리 상태를 선택하세요.");
    if (!requests.some(request => request.id === id)) throw new ValidationError("수정 요청을 찾을 수 없습니다.");
    return requests.map(request => request.id === id ? { ...request, status } : request);
  }

  return { ValidationError, normalizeContract, normalizeRequest, evaluateRequests, updateStatus };
});
