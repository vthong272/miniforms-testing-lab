"""Verify that every generated mutant is structural single-fault and non-equivalent."""

import base64
import csv
import json
import subprocess
from pathlib import Path

from scripts.mutant_definitions import MUTANTS
from tests.frozen_cases import ALL_CASES


ROOT = Path(__file__).resolve().parents[1]


def _js_input(case):
    if case["form"] == "registration":
        return {
            "username": case["username"], "email": case["email"], "age": case["age"],
            "password": case["password"], "confirmPassword": case["confirm_password"],
        }
    if case["form"] == "shipping":
        return {
            "customerType": case["customer_type"], "orderValue": case["order_value"],
            "region": case["region"], "couponStatus": case["coupon_status"],
        }
    return {
        "age": case["age"], "monthlyIncome": case["monthly_income"],
        "creditScore": case["credit_score"], "employmentStatus": case["employment_status"],
        "requestedLoan": case["requested_loan"],
    }


def verify_mutant(mutant, cases_by_id):
    golden_path = ROOT / "app" / "js" / f"{mutant['target']}.js"
    mutant_path = ROOT / "app" / "mutants" / mutant["id"] / f"{mutant['target']}.js"
    golden = golden_path.read_text(encoding="utf-8")
    generated = mutant_path.read_text(encoding="utf-8").split("\n", 1)[1]
    if golden.count(mutant["old"]) != 1:
        raise ValueError(f"{mutant['id']}: mutation target is not unique in golden source")
    expected = golden.replace(mutant["old"], mutant["new"], 1)
    if generated != expected:
        raise ValueError(f"{mutant['id']}: generated module contains more than its registered change")

    case = cases_by_id[mutant["witness_test_id"]]
    encoded = base64.urlsafe_b64encode(
        json.dumps(_js_input(case)).encode("utf-8")
    ).decode("ascii")
    process = subprocess.run(
        ["node", str(ROOT / "scripts" / "compare_variant.mjs"), str(golden_path),
         str(mutant_path), mutant["target"], encoded],
        check=True, capture_output=True, text=True,
    )
    comparison = json.loads(process.stdout)
    if not comparison["differs"]:
        raise ValueError(f"{mutant['id']}: equivalent for witness {case['test_id']}")
    return comparison


def main():
    cases_by_id = {case["test_id"]: case for case in ALL_CASES}
    verified = []
    for mutant in MUTANTS:
        comparison = verify_mutant(mutant, cases_by_id)
        verified.append({
            "id": mutant["id"], "form": mutant["form"], "target": mutant["target"],
            "category": mutant["category"], "requirement": mutant["requirement"],
            "description": mutant["description"], "witness_test_id": mutant["witness_test_id"],
            "single_fault": True, "behavior_differs_from_golden": True,
            "witness_golden_output": comparison["golden"],
            "witness_mutant_output": comparison["mutant"],
        })

    (ROOT / "mutant-manifest.json").write_text(
        json.dumps(verified, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    csv_rows = [{key: value for key, value in row.items()
                 if key not in {"witness_golden_output", "witness_mutant_output"}}
                for row in verified]
    with (ROOT / "mutant-manifest.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(csv_rows[0]))
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"Verified {len(verified)} non-equivalent single-fault mutants.")


if __name__ == "__main__":
    main()
