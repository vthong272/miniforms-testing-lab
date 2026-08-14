"""Execute and classify the frozen Selenium suites against app variants."""

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

from scripts.mutant_definitions import MUTANTS


ROOT = Path(__file__).resolve().parents[1]
SUITES = {"EP": ("ep", 30), "BVA": ("bva", 51), "DTT": ("dtt", 29)}
FROZEN_SHA256 = "5cbd9e3b0e0b1aa0ef5e9f549eb09e0709fbb3093eccbff14a4c9ce24d8a9131"


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


def _start_server():
    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1",
         "--directory", str(ROOT / "app")],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(100):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8765/", timeout=1) as response:
                if response.status == 200 and b"MiniForms Testing Lab" in response.read():
                    return process
        except OSError:
            time.sleep(0.1)
    process.terminate()
    raise RuntimeError("Experiment server did not start")


def run_suite(variant, suite, marker, expected, output_dir):
    junit = output_dir / "junit" / variant / f"{suite}.xml"
    log = output_dir / "logs" / variant / f"{suite}.log"
    junit.parent.mkdir(parents=True, exist_ok=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["MINIFORMS_URL"] = "http://127.0.0.1:8765/"
    env["MINIFORMS_VARIANT"] = variant
    command = [
        sys.executable, "-m", "pytest", "tests/selenium/test_frozen_golden.py",
        "-m", marker, "-q", "-p", "no:cacheprovider", f"--junitxml={junit}",
    ]
    started = time.perf_counter()
    process = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
    elapsed = time.perf_counter() - started
    log.write_text(
        f"command: {' '.join(command)}\nreturn_code: {process.returncode}\n"
        f"elapsed_seconds: {elapsed:.3f}\n\nSTDOUT\n{process.stdout}\nSTDERR\n{process.stderr}",
        encoding="utf-8",
    )
    return {
        "variant": variant, "suite": suite,
        "status": classify_junit(junit, expected),
        "return_code": process.returncode, "elapsed_seconds": round(elapsed, 3),
        "junit": str(junit.relative_to(ROOT)), "log": str(log.relative_to(ROOT)),
    }


def run_variant(variant, output_dir):
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [
            pool.submit(run_suite, variant, suite, marker, expected, output_dir)
            for suite, (marker, expected) in SUITES.items()
        ]
        results = [future.result() for future in futures]
    invalid = [result for result in results if result["status"] == "invalid"]
    if invalid:
        labels = ", ".join(f"{item['variant']}/{item['suite']}" for item in invalid)
        raise RuntimeError(f"Invalid infrastructure/test execution: {labels}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = (args.output or ROOT / "experiment-results" / f"run-{timestamp}").resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise RuntimeError(f"Refusing to reuse non-empty result directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    actual_hash = hashlib.sha256((ROOT / "tests" / "frozen_cases.py").read_bytes()).hexdigest()
    if actual_hash != FROZEN_SHA256:
        raise RuntimeError(f"Frozen manifest hash mismatch: {actual_hash}")

    server = _start_server()
    all_runs = []
    try:
        golden = run_variant("golden", output_dir)
        if any(result["status"] != "alive" for result in golden):
            raise RuntimeError("Golden gate failed; mutant execution was not started")
        all_runs.extend(golden)
        print("golden: EP 30/30, BVA 51/51, DTT 29/29", flush=True)

        rows = []
        for mutant in MUTANTS:
            results = run_variant(mutant["id"], output_dir)
            all_runs.extend(results)
            status = {result["suite"]: result["status"] for result in results}
            row = {
                "Mutant": mutant["id"], "Form": mutant["form"],
                "Category": mutant["category"],
                **{suite: int(status[suite] == "killed") for suite in SUITES},
                "Valid": 1, "Witness": mutant["witness_test_id"],
            }
            rows.append(row)
            print(f"{mutant['id']}: EP={row['EP']} BVA={row['BVA']} DTT={row['DTT']}", flush=True)
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    matrix = output_dir / "mutation-matrix.csv"
    with matrix.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "started_utc": timestamp, "completed_utc": datetime.now(timezone.utc).isoformat(),
        "frozen_tag": "frozen-v1.0", "frozen_commit": "431bcf8",
        "frozen_sha256": actual_hash, "suite_sizes": {key: value[1] for key, value in SUITES.items()},
        "mutants": len(rows), "runs": all_runs,
    }
    (output_dir / "run-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Results: {output_dir}")


if __name__ == "__main__":
    main()
