import csv
import os
import tempfile
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = os.getenv("MINIFORMS_URL", "http://localhost:8000/")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "test-design" / "bva-registration.csv"


def load_bva_cases():
    with DATASET_PATH.open(encoding="utf-8", newline="") as dataset:
        return list(csv.DictReader(dataset))


BVA_CASES = load_bva_cases()


@pytest.fixture(scope="module")
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


@pytest.mark.parametrize("case", BVA_CASES, ids=lambda case: case["test_id"])
def test_registration_boundary_values(driver, case):
    driver.get(BASE_URL)

    driver.find_element(By.ID, "reg-username").send_keys(case["username"])
    driver.find_element(By.ID, "reg-email").send_keys(case["email"])
    driver.find_element(By.ID, "reg-age").send_keys(case["age"])
    driver.find_element(By.ID, "reg-password").send_keys(case["password"])
    driver.find_element(By.ID, "reg-confirm-password").send_keys(
        case["confirm_password"]
    )
    driver.find_element(By.ID, "registration-submit").click()

    result = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "registration-result"))
    )
    assert result.text.startswith(case["expected_result"]), (
        f'{case["test_id"]}: expected {case["expected_result"]}, '
        f"but received {result.text!r}"
    )


def test_dataset_contains_exactly_eighteen_balanced_cases():
    assert len(BVA_CASES) == 18
    assert sum(case["field"] == "username" for case in BVA_CASES) == 6
    assert sum(case["field"] == "age" for case in BVA_CASES) == 6
    assert sum(case["field"] == "password_length" for case in BVA_CASES) == 6
