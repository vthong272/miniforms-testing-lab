from collections import Counter

from tests.frozen_cases import ALL_CASES


def test_frozen_manifest_has_exactly_110_unique_cases():
    assert len(ALL_CASES) == 110
    assert len({case["test_id"] for case in ALL_CASES}) == 110
    assert Counter(case["technique"] for case in ALL_CASES) == {
        "EP": 30,
        "BVA": 51,
        "DTT": 29,
    }


def test_every_frozen_case_is_traceable_and_executable():
    valid_forms = {"registration", "shipping", "loan"}
    for case in ALL_CASES:
        assert case["form"] in valid_forms, case["test_id"]
        assert case["requirement_id"], case["test_id"]
        assert case["expected_result"] in {
            "Accepted",
            "Rejected",
            "Calculated",
            "Approved",
        }, case["test_id"]
