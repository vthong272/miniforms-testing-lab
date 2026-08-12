import { validateRegistration } from "./registration.js";
import { calculateOrder } from "./shipping.js";
import { evaluateLoan } from "./loan.js";

const navItems = [...document.querySelectorAll(".nav-item")];
const panels = [...document.querySelectorAll(".form-panel")];
const currency = new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" });

function activatePanel(targetId, updateHash = true) {
  if (!panels.some((panel) => panel.id === targetId)) return;

  panels.forEach((panel) => {
    const active = panel.id === targetId;
    panel.hidden = !active;
    panel.classList.toggle("is-active", active);
  });
  navItems.forEach((item) => {
    const active = item.dataset.target === targetId;
    item.classList.toggle("is-active", active);
    if (active) item.setAttribute("aria-current", "page");
    else item.removeAttribute("aria-current");
  });
  if (updateHash) history.replaceState(null, "", `#${targetId}`);
}

navItems.forEach((item) => {
  item.addEventListener("click", () => activatePanel(item.dataset.target));
});

function resetResult(resultElement, state) {
  resultElement.replaceChildren();
  resultElement.className = `result-box ${state}`;
}

function renderMessage(resultElement, state, title, details = []) {
  resetResult(resultElement, state);
  const heading = document.createElement("strong");
  heading.textContent = title;
  resultElement.append(heading);

  if (details.length > 0) {
    const list = document.createElement("ul");
    details.forEach((detail) => {
      const item = document.createElement("li");
      item.textContent = detail;
      list.append(item);
    });
    resultElement.append(list);
  }
}

document.querySelector("#registration-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  const result = validateRegistration(data);
  const output = document.querySelector("#registration-result");

  if (result.accepted) {
    renderMessage(output, "is-success", "Accepted — registration data satisfies all five rules.");
  } else {
    renderMessage(output, "is-error", `Rejected — ${result.errors.length} rule(s) failed.`, result.errors);
  }
});

document.querySelector("#shipping-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  const result = calculateOrder(data);
  const output = document.querySelector("#shipping-result");

  if (!result.valid) {
    renderMessage(output, "is-error", "Unable to calculate order.", result.errors);
    return;
  }

  resetResult(output, "is-success");
  const heading = document.createElement("strong");
  heading.textContent = "Calculation completed.";
  const metrics = document.createElement("div");
  metrics.className = "metrics";
  [
    ["Discount", `${result.discountRate * 100}% (${currency.format(result.discountAmount)})`],
    ["Shipping", currency.format(result.shippingFee)],
    ["Final amount", currency.format(result.finalAmount)],
  ].forEach(([label, value]) => {
    const metric = document.createElement("div");
    metric.className = "metric";
    const metricLabel = document.createElement("span");
    const metricValue = document.createElement("strong");
    metricLabel.textContent = label;
    metricValue.textContent = value;
    metric.append(metricLabel, metricValue);
    metrics.append(metric);
  });
  output.append(heading, metrics);
});

document.querySelector("#loan-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  const result = evaluateLoan(data);
  const output = document.querySelector("#loan-result");

  if (result.approved) {
    renderMessage(output, "is-success", "Approved — the applicant satisfies all five conditions.");
  } else {
    renderMessage(output, "is-error", `Rejected — ${result.reasons.length} condition(s) failed.`, result.reasons);
  }
});

const initialTarget = window.location.hash.slice(1);
activatePanel(initialTarget || "registration", false);
