import re
from decimal import Decimal, ROUND_HALF_UP

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def submit_case(driver, base_url, case):
    form = case["form"]
    driver.get(base_url)
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "registration"))
    )
    if form != "registration":
        driver.find_element(By.CSS_SELECTOR, f'[data-target="{form}"]').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, form))
    )
    if form == "registration":
        _fill_registration(driver, case)
    elif form == "shipping":
        _fill_shipping(driver, case)
    elif form == "loan":
        _fill_loan(driver, case)
    else:
        raise AssertionError(f"Unknown form: {form}")

    result = WebDriverWait(driver, 5).until(
        lambda browser: browser.find_element(By.ID, f"{form}-result")
    )
    _assert_result(case, result.text)


def _type(driver, element_id, value):
    element = driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(str(value))


def _fill_registration(driver, case):
    _type(driver, "reg-username", case["username"])
    _type(driver, "reg-email", case["email"])
    _type(driver, "reg-age", case["age"])
    _type(driver, "reg-password", case["password"])
    _type(driver, "reg-confirm-password", case["confirm_password"])
    driver.find_element(By.ID, "registration-submit").click()


def _fill_shipping(driver, case):
    _select_or_inject(driver, "ship-customer-type", case["customer_type"])
    _type(driver, "ship-order-value", case["order_value"])
    _select_or_inject(driver, "ship-region", case["region"])
    _select_or_inject(driver, "ship-coupon-status", case["coupon_status"])
    driver.find_element(By.ID, "shipping-submit").click()


def _fill_loan(driver, case):
    _type(driver, "loan-age", case["age"])
    _type(driver, "loan-income", case["monthly_income"])
    _type(driver, "loan-credit-score", case["credit_score"])
    Select(driver.find_element(By.ID, "loan-employment")).select_by_value(
        case["employment_status"]
    )
    _type(driver, "loan-requested", case["requested_loan"])
    driver.find_element(By.ID, "loan-submit").click()


def _select_or_inject(driver, element_id, value):
    select = driver.find_element(By.ID, element_id)
    try:
        Select(select).select_by_value(value)
    except Exception:
        driver.execute_script(
            "arguments[0].add(new Option(arguments[1], arguments[1], true, true));",
            select,
            value,
        )


def _number(text):
    return Decimal(re.sub(r"[^0-9,.-]", "", text).replace(".", "").replace(",", "."))


def _assert_result(case, result_text):
    expected = case["expected_result"]
    if expected == "Rejected" and case["form"] == "shipping":
        assert result_text.startswith("Unable to calculate order."), (
            f"{case['test_id']}: expected rejection, got {result_text!r}"
        )
        return
    if expected in {"Accepted", "Rejected", "Approved"}:
        assert result_text.startswith(expected), (
            f"{case['test_id']}: expected {expected}, got {result_text!r}"
        )
        return

    assert result_text.startswith("Calculation completed."), (
        f"{case['test_id']}: expected a calculation, got {result_text!r}"
    )
    discount_match = re.search(r"DISCOUNT\s+(\d+(?:\.\d+)?)%", result_text, re.I)
    shipping_match = re.search(r"SHIPPING\s+([^\n]+)", result_text, re.I)
    final_match = re.search(r"FINAL AMOUNT\s+([^\n]+)", result_text, re.I)
    assert discount_match and shipping_match and final_match, result_text
    assert Decimal(discount_match.group(1)) == Decimal(case["expected_discount_rate"])
    assert _number(shipping_match.group(1)) == Decimal(case["expected_shipping_fee"])
    expected_final = Decimal(case["expected_final_amount"]).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )
    assert _number(final_match.group(1)) == expected_final
