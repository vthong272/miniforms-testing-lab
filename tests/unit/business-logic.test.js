import test from "node:test";
import assert from "node:assert/strict";

import { validateRegistration } from "../../app/js/registration.js";
import { calculateOrder } from "../../app/js/shipping.js";
import { evaluateLoan } from "../../app/js/loan.js";

test("registration accepts all valid boundary values", () => {
  const result = validateRegistration({
    username: "minhnguyen",
    email: "minh@example.com",
    age: 18,
    password: "Test1234",
    confirmPassword: "Test1234",
  });

  assert.equal(result.accepted, true);
  assert.deepEqual(result.errors, []);
});

test("registration reports every invalid input class", () => {
  const result = validateRegistration({
    username: "abc",
    email: "invalid-email",
    age: 61,
    password: "short",
    confirmPassword: "different",
  });

  assert.equal(result.accepted, false);
  assert.equal(result.errors.length, 5);
});

test("shipping applies ten-percent VIP discount at one million", () => {
  const result = calculateOrder({
    customerType: "vip",
    orderValue: 1_000_000,
    region: "local",
    couponStatus: "none",
  });

  assert.equal(result.discountRate, 0.1);
  assert.equal(result.shippingFee, 0);
  assert.equal(result.finalAmount, 900_000);
});

test("shipping uses only the highest eligible discount", () => {
  const result = calculateOrder({
    customerType: "vip",
    orderValue: 1_200_000,
    region: "remote",
    couponStatus: "valid",
  });

  assert.equal(result.discountRate, 0.1);
  assert.equal(result.shippingFee, 50_000);
  assert.equal(result.finalAmount, 1_130_000);
});

test("loan approves an applicant who meets every business rule", () => {
  const result = evaluateLoan({
    age: 21,
    monthlyIncome: 15_000_000,
    creditScore: 650,
    employmentStatus: "employed",
    requestedLoan: 150_000_000,
  });

  assert.equal(result.approved, true);
  assert.deepEqual(result.reasons, []);
});

test("loan reports all failed decision conditions", () => {
  const result = evaluateLoan({
    age: 20,
    monthlyIncome: 14_000_000,
    creditScore: 649,
    employmentStatus: "unemployed",
    requestedLoan: 150_000_000,
  });

  assert.equal(result.approved, false);
  assert.equal(result.reasons.length, 5);
});
