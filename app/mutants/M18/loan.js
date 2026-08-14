// M18: Loan positivity and upper-limit checks use AND instead of OR
export function evaluateLoan(input) {
  const age = Number(input.age);
  const monthlyIncome = Number(input.monthlyIncome);
  const creditScore = Number(input.creditScore);
  const employmentStatus = String(input.employmentStatus ?? "").toLowerCase();
  const requestedLoan = Number(input.requestedLoan);
  const reasons = [];

  if (!Number.isInteger(age) || age < 21 || age > 60) {
    reasons.push("Age must be an integer from 21 to 60.");
  }
  if (!Number.isFinite(monthlyIncome) || monthlyIncome < 15_000_000) {
    reasons.push("Monthly income must be at least 15,000,000 VND.");
  }
  if (!Number.isInteger(creditScore) || creditScore < 650 || creditScore > 850) {
    reasons.push("Credit score must be an integer from 650 to 850.");
  }
  if (employmentStatus !== "employed") {
    reasons.push("Applicant must be employed.");
  }
  if (!Number.isFinite(requestedLoan) || requestedLoan <= 0 && requestedLoan > monthlyIncome * 10) {
    reasons.push("Requested loan must be positive and no more than 10 times monthly income.");
  }

  return { approved: reasons.length === 0, reasons };
}
