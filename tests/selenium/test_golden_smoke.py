import os
import tempfile
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


BASE_URL = os.getenv("MINIFORMS_URL", "http://localhost:8000/")
PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def driver():
    with tempfile.TemporaryDirectory(prefix=".selenium-profile-", dir=PROJECT_ROOT) as profile:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,900")
        options.add_argument(f"--user-data-dir={profile}")
        browser = webdriver.Chrome(options=options)
        yield browser
        browser.quit()


def test_three_golden_happy_paths(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 5)

    driver.find_element(By.ID, "reg-username").send_keys("minhnguyen")
    driver.find_element(By.ID, "reg-email").send_keys("minh@example.com")
    driver.find_element(By.ID, "reg-age").send_keys("18")
    driver.find_element(By.ID, "reg-password").send_keys("Test1234")
    driver.find_element(By.ID, "reg-confirm-password").send_keys("Test1234")
    driver.find_element(By.ID, "registration-submit").click()
    assert "Accepted" in wait.until(
        EC.visibility_of_element_located((By.ID, "registration-result"))
    ).text

    driver.find_element(By.CSS_SELECTOR, '[data-target="shipping"]').click()
    Select(driver.find_element(By.ID, "ship-customer-type")).select_by_value("vip")
    driver.find_element(By.ID, "ship-order-value").send_keys("1000000")
    Select(driver.find_element(By.ID, "ship-region")).select_by_value("local")
    driver.find_element(By.ID, "shipping-submit").click()
    shipping_result = wait.until(
        EC.visibility_of_element_located((By.ID, "shipping-result"))
    ).text
    assert "10%" in shipping_result
    assert "900.000" in shipping_result

    driver.find_element(By.CSS_SELECTOR, '[data-target="loan"]').click()
    assert driver.current_url.endswith("#loan")
    wait.until(EC.visibility_of_element_located((By.ID, "loan")))
    assert not driver.find_element(By.ID, "shipping").is_displayed()
    assert driver.find_element(By.CSS_SELECTOR, '[data-target="loan"]').get_attribute(
        "aria-current"
    ) == "page"
    driver.find_element(By.ID, "loan-age").send_keys("21")
    driver.find_element(By.ID, "loan-income").send_keys("15000000")
    driver.find_element(By.ID, "loan-credit-score").send_keys("650")
    driver.find_element(By.ID, "loan-requested").send_keys("150000000")
    driver.find_element(By.ID, "loan-submit").click()
    assert "Approved" in wait.until(
        EC.visibility_of_element_located((By.ID, "loan-result"))
    ).text
