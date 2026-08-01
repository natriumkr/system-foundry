import test from "node:test";
import assert from "node:assert/strict";
import { buildCsv, calculateEconomics, parseInputs } from "../app/calculator.js";

const sample = {
  sellingPrice: 39000,
  productCost: 14000,
  inboundShipping: 800,
  outboundShipping: 3200,
  packagingCost: 700,
  returnHandlingCost: 2500,
  platformFeePct: 10.8,
  paymentFeePct: 2.9,
  adCostPct: 7,
  vatReservePct: 3,
  returnRatePct: 6,
  targetMarginPct: 25,
  monthlyOrders: 180,
  fixedMonthlyCost: 450000,
};

test("calculates unit economics including expected return and fixed costs", () => {
  const result = calculateEconomics(sample);
  assert.equal(result.returnExpectedCost, 342);
  assert.equal(result.fixedCostPerOrder, 2500);
  assert.ok(Math.abs(result.unitProfit - 8215) < 0.001);
  assert.ok(Math.abs(result.monthlyProfit - 1478700) < 0.001);
});

test("reverse target price reaches requested margin", () => {
  const result = calculateEconomics(sample);
  const rerun = calculateEconomics({ ...sample, sellingPrice: result.targetPrice });
  assert.ok(Math.abs(rerun.marginPct - sample.targetMarginPct) < 0.000001);
});

test("break-even price produces zero unit profit", () => {
  const result = calculateEconomics(sample);
  const rerun = calculateEconomics({ ...sample, sellingPrice: result.breakEvenPrice });
  assert.ok(Math.abs(rerun.unitProfit) < 0.000001);
});

test("rejects invalid percentages and non-integer monthly orders", () => {
  assert.throws(() => parseInputs({ ...sample, adCostPct: 101 }), /between 0 and 100/);
  assert.throws(() => parseInputs({ ...sample, monthlyOrders: 3.5 }), /positive integer/);
});

test("returns null target price when target is mathematically impossible", () => {
  const result = calculateEconomics({ ...sample, targetMarginPct: 80 });
  assert.equal(result.targetPrice, null);
});

test("exports a BOM-free, structured CSV body", () => {
  const csv = buildCsv(calculateEconomics(sample));
  assert.match(csv, /^Metric,Value/);
  assert.match(csv, /Unit profit,8215/);
  assert.equal(csv.split("\n").length, 10);
});
