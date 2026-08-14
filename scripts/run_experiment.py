"""Execute and classify the frozen Selenium suites against app variants."""

from pathlib import Path
import xml.etree.ElementTree as ET


def classify_junit(report_path: Path, expected_tests: int) -> str:
    if not report_path.exists():
        return "invalid"
    try:
        root = ET.parse(report_path).getroot()
    except ET.ParseError:
        return "invalid"
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    if not suites:
        return "invalid"
    tests = sum(int(suite.get("tests", 0)) for suite in suites)
    failures = sum(int(suite.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.get("errors", 0)) for suite in suites)
    skipped = sum(int(suite.get("skipped", 0)) for suite in suites)
    if tests != expected_tests or errors or skipped:
        return "invalid"
    return "killed" if failures else "alive"
