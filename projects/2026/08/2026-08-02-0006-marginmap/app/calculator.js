const PERCENT_FIELDS = [
  "platformFeePct",
  "paymentFeePct",
  "adCostPct",
  "vatReservePct",
  "returnRatePct",
  "targetMarginPct",
];

const NON_NEGATIVE_FIELDS = [
  "sellingPrice",
  "productCost",
  "inboundShipping",
  "outboundShipping",
  "packagingCost",
  "returnHandlingCost",
  "monthlyOrders",
  "fixedMonthlyCost",
];

export function parseInputs(raw) {
  const values = {};
  const fields = [...NON_NEGATIVE_FIELDS, ...PERCENT_FIELDS];

  for (const field of fields) {
    const value = Number(raw[field]);
    if (!Number.isFinite(value)) {
      throw new Error(`${field} must be a finite number`);
    }
    values[field] = value;
  }

  for (const field of NON_NEGATIVE_FIELDS) {
    if (values[field] < 0) throw new Error(`${field} cannot be negative`);
  }

  for (const field of PERCENT_FIELDS) {
    if (values[field] < 0 || values[field] > 100) {
      throw new Error(`${field} must be between 0 and 100`);
    }
  }

  if (values.sellingPrice <= 0) throw new Error("sellingPrice must be greater than zero");
  if (!Number.isInteger(values.monthlyOrders) || values.monthlyOrders <= 0) {
    throw new Error("monthlyOrders must be a positive integer");
  }

  return values;
}

export function calculateEconomics(raw) {
  const v = parseInputs(raw);
  const ratePct = v.platformFeePct + v.paymentFeePct + v.adCostPct + v.vatReservePct;
  const rate = ratePct / 100;
  const variableFees = v.sellingPrice * rate;
  const returnExpectedCost = (v.returnRatePct / 100) *
    (v.outboundShipping + v.returnHandlingCost);
  const fixedCostPerOrder = v.fixedMonthlyCost / v.monthlyOrders;
  const baseUnitCost = v.productCost + v.inboundShipping + v.outboundShipping +
    v.packagingCost + returnExpectedCost;
  const totalUnitCost = baseUnitCost + variableFees + fixedCostPerOrder;
  const unitProfit = v.sellingPrice - totalUnitCost;
  const marginPct = (unitProfit / v.sellingPrice) * 100;
  const monthlyProfit = unitProfit * v.monthlyOrders;

  const breakEvenDenominator = 1 - rate;
  const targetDenominator = 1 - rate - (v.targetMarginPct / 100);
  const allocatedBaseCost = baseUnitCost + fixedCostPerOrder;

  const breakEvenPrice = breakEvenDenominator > 0
    ? allocatedBaseCost / breakEvenDenominator
    : null;
  const targetPrice = targetDenominator > 0
    ? allocatedBaseCost / targetDenominator
    : null;

  return {
    ...v,
    ratePct,
    variableFees,
    returnExpectedCost,
    fixedCostPerOrder,
    baseUnitCost,
    totalUnitCost,
    unitProfit,
    marginPct,
    monthlyProfit,
    breakEvenPrice,
    targetPrice,
  };
}

export function buildCsv(result) {
  const rows = [
    ["Metric", "Value (KRW or %)"] ,
    ["Selling price", result.sellingPrice],
    ["Total unit cost", round(result.totalUnitCost)],
    ["Unit profit", round(result.unitProfit)],
    ["Profit margin (%)", round(result.marginPct, 2)],
    ["Monthly profit", round(result.monthlyProfit)],
    ["Break-even price", nullableRound(result.breakEvenPrice)],
    ["Target price", nullableRound(result.targetPrice)],
    ["Expected return cost/order", round(result.returnExpectedCost)],
    ["Fixed cost/order", round(result.fixedCostPerOrder)],
  ];

  return rows.map((row) => row.map(csvEscape).join(",")).join("\n");
}

function round(value, digits = 0) {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function nullableRound(value) {
  return value === null ? "Unavailable" : round(value);
}

function csvEscape(value) {
  const text = String(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}
