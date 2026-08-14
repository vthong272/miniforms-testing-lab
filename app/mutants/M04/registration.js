// M04: Maximum age uses < 60 instead of <= 60
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function validateRegistration(input) {
  const username = String(input.username ?? "").trim();
  const email = String(input.email ?? "").trim();
  const age = Number(input.age);
  const password = String(input.password ?? "");
  const confirmPassword = String(input.confirmPassword ?? "");
  const errors = [];

  if (username.length < 5 || username.length > 15) {
    errors.push("Username must contain 5 to 15 characters.");
  }
  if (!EMAIL_PATTERN.test(email)) {
    errors.push("Email must have a valid format.");
  }
  if (!Number.isInteger(age) || age < 18 || age >= 60) {
    errors.push("Age must be an integer from 18 to 60.");
  }
  if (password.length < 8 || password.length > 20) {
    errors.push("Password must contain 8 to 20 characters.");
  }
  if (password !== confirmPassword) {
    errors.push("Password and confirmation must match.");
  }

  return { accepted: errors.length === 0, errors };
}
