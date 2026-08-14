"""Generate the 18 pre-registered mutant modules and manifests."""

import csv
import json
from pathlib import Path

from scripts.mutant_definitions import MUTANTS


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
MUTANTS_DIR = APP / "mutants"


def main():
    MUTANTS_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    for mutant in MUTANTS:
        source = (APP / "js" / f"{mutant['target']}.js").read_text(encoding="utf-8")
        count = source.count(mutant["old"])
        if count != 1:
            raise ValueError(f"{mutant['id']}: expected one replacement target, found {count}")
        output = source.replace(mutant["old"], mutant["new"], 1)
        folder = MUTANTS_DIR / mutant["id"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{mutant['target']}.js"
        path.write_text(f"// {mutant['id']}: {mutant['description']}\n{output}", encoding="utf-8")
        generated.append({
            "id": mutant["id"], "form": mutant["form"], "target": mutant["target"],
            "category": mutant["category"], "requirement": mutant["requirement"],
            "description": mutant["description"], "witness_test_id": mutant["witness_test_id"],
            "single_fault": True, "behavior_differs_from_golden": None,
        })

    (ROOT / "mutant-manifest.json").write_text(
        json.dumps(generated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    fields = list(generated[0])
    with (ROOT / "mutant-manifest.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(generated)
    print(f"Generated {len(generated)} single-fault mutants.")


if __name__ == "__main__":
    main()
