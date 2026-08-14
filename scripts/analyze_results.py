"""Calculate mutation-testing metrics from a completed matrix."""

import argparse
import csv
import json
from pathlib import Path


SUITE_SIZES = {"EP": 30, "BVA": 51, "DTT": 29}
CATEGORIES = ["Partition", "Boundary", "Decision-rule"]


def calculate_metrics(rows, suite_sizes=SUITE_SIZES):
    valid = [row for row in rows if int(row.get("Valid", 1)) == 1]
    total = len(valid)
    killed_sets = {
        suite: {row["Mutant"] for row in valid if int(row[suite]) == 1}
        for suite in suite_sizes
    }
    suites = {}
    for suite, size in suite_sizes.items():
        killed = len(killed_sets[suite])
        by_category = {}
        for category in CATEGORIES:
            category_rows = [row for row in valid if row["Category"] == category]
            category_killed = sum(int(row[suite]) for row in category_rows)
            by_category[category] = {
                "killed": category_killed, "valid": len(category_rows),
                "ddr_percent": round(100 * category_killed / len(category_rows), 2),
            }
        suites[suite] = {
            "test_cases": size, "killed": killed, "valid_mutants": total,
            "ddr_percent": round(100 * killed / total, 2),
            "efficiency": round(killed / size, 4), "by_category": by_category,
        }

    overlaps = {}
    names = list(suite_sizes)
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            intersection = killed_sets[left] & killed_sets[right]
            union = killed_sets[left] | killed_sets[right]
            overlaps[f"{left}-{right}"] = {
                "count": len(intersection), "mutants": sorted(intersection),
                "jaccard_percent": round(100 * len(intersection) / len(union), 2) if union else 0,
            }
    unique = {
        suite: sorted(killed_sets[suite] - set().union(
            *(killed_sets[other] for other in names if other != suite)
        )) for suite in names
    }
    combined = set().union(*killed_sets.values())
    return {
        "valid_mutants": total, "suites": suites, "overlap": overlaps,
        "unique": {suite: {"count": len(ids), "mutants": ids} for suite, ids in unique.items()},
        "combined": {"killed": len(combined), "valid_mutants": total,
                     "ddr_percent": round(100 * len(combined) / total, 2),
                     "mutants": sorted(combined)},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result_dir", type=Path)
    args = parser.parse_args()
    with (args.result_dir / "mutation-matrix.csv").open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    metrics = calculate_metrics(rows)
    (args.result_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
