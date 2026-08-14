from pathlib import Path

from scripts.run_experiment import classify_junit


def write_junit(path: Path, *, tests=3, failures=0, errors=0, skipped=0):
    path.write_text(
        f'<testsuites><testsuite tests="{tests}" failures="{failures}" '
        f'errors="{errors}" skipped="{skipped}" /></testsuites>',
        encoding="utf-8",
    )


def test_assertion_failure_kills_mutant(tmp_path):
    report = tmp_path / "failure.xml"
    write_junit(report, failures=1)
    assert classify_junit(report, expected_tests=3) == "killed"


def test_all_passing_tests_leave_mutant_alive(tmp_path):
    report = tmp_path / "pass.xml"
    write_junit(report)
    assert classify_junit(report, expected_tests=3) == "alive"


def test_setup_or_collection_error_is_invalid_not_killed(tmp_path):
    report = tmp_path / "error.xml"
    write_junit(report, tests=0, errors=1)
    assert classify_junit(report, expected_tests=3) == "invalid"


def test_missing_or_incomplete_report_is_invalid(tmp_path):
    assert classify_junit(tmp_path / "missing.xml", expected_tests=3) == "invalid"
    report = tmp_path / "incomplete.xml"
    write_junit(report, tests=2)
    assert classify_junit(report, expected_tests=3) == "invalid"
