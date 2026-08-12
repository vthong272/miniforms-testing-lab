import pytest

from tests.frozen_cases import BVA_CASES, DTT_CASES, EP_CASES
from tests.selenium.conftest import BASE_URL
from tests.selenium.form_runner import submit_case


@pytest.mark.ep
@pytest.mark.parametrize("case", EP_CASES, ids=lambda case: case["test_id"])
def test_ep_case_passes_on_golden(driver, case):
    submit_case(driver, BASE_URL, case)


@pytest.mark.bva
@pytest.mark.parametrize("case", BVA_CASES, ids=lambda case: case["test_id"])
def test_bva_case_passes_on_golden(driver, case):
    submit_case(driver, BASE_URL, case)


@pytest.mark.dtt
@pytest.mark.parametrize("case", DTT_CASES, ids=lambda case: case["test_id"])
def test_dtt_case_passes_on_golden(driver, case):
    submit_case(driver, BASE_URL, case)
