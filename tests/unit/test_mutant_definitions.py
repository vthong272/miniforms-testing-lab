from collections import Counter

from scripts.mutant_definitions import MUTANTS


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
