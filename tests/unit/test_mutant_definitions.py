from collections import Counter

from scripts.mutant_definitions import MUTANTS
from scripts.verify_mutants import verify_mutant
from tests.frozen_cases import ALL_CASES


def test_eighteen_mutants_are_balanced_by_category_and_form():
    assert len(MUTANTS) == 18
    assert len({mutant["id"] for mutant in MUTANTS}) == 18
    assert Counter(mutant["category"] for mutant in MUTANTS) == {
        "Partition": 6,
        "Boundary": 6,
        "Decision-rule": 6,
    }
    assert Counter(mutant["form"] for mutant in MUTANTS) == {
        "Registration": 6,
        "Shipping": 6,
        "Loan": 6,
    }


def test_every_mutant_has_one_target_and_a_frozen_witness():
    for mutant in MUTANTS:
        assert mutant["target"] in {"registration", "shipping", "loan"}
        assert mutant["old"] != mutant["new"]
        assert mutant["witness_test_id"]


def test_generated_mutants_are_single_fault_and_non_equivalent():
    cases_by_id = {case["test_id"]: case for case in ALL_CASES}
    for mutant in MUTANTS:
        assert verify_mutant(mutant, cases_by_id)["differs"] is True
