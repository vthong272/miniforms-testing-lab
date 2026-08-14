// M11: VIP discount eligibility uses OR instead of AND
const LOCAL_SHIPPING_FEE = 30_000;
const REMOTE_SHIPPING_FEE = 50_000;

export function calculateOrder(input) {
  const customerType = String(input.customerType ?? "").toLowerCase();
  const region = String(input.region ?? "").toLowerCase();
  const couponStatus = String(input.couponStatus ?? "").toLowerCase();
  const orderValue = Number(input.orderValue);
  const errors = [];

  if (!Number.isFinite(orderValue) || orderValue <= 0) {
    errors.push("Order value must be greater than zero.");
  }
  if (!["regular", "vip"].includes(customerType)) {
    errors.push("Customer type is invalid.");
  }
  if (!["local", "remote"].includes(region)) {
    errors.push("Shipping region is invalid.");
  }
  if (!["none", "valid", "invalid"].includes(couponStatus)) {
    errors.push("Coupon status is invalid.");
  }
  if (errors.length > 0) {
    return { valid: false, errors };
  }

  const vipDiscount = customerType === "vip" || orderValue >= 1_000_000 ? 0.1 : 0;
  const couponDiscount = couponStatus === "valid" && orderValue >= 500_000 ? 0.05 : 0;
  const discountRate = Math.max(vipDiscount, couponDiscount);
  const shippingFee = region === "local" && orderValue >= 800_000
    ? 0
    : region === "remote" ? REMOTE_SHIPPING_FEE : LOCAL_SHIPPING_FEE;
  const discountAmount = orderValue * discountRate;

  return {
    valid: true,
    errors: [],
    discountRate,
    discountAmount,
    shippingFee,
    finalAmount: orderValue - discountAmount + shippingFee,
  };
}
