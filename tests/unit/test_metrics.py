from scripts.analyze_results import calculate_metrics


def test_metrics_include_ddr_efficiency_overlap_unique_and_combined():
    rows = [
        {"Mutant": "M01", "Category": "Partition", "EP": 1, "BVA": 0, "DTT": 1, "Valid": 1},
        {"Mutant": "M02", "Category": "Boundary", "EP": 0, "BVA": 1, "DTT": 0, "Valid": 1},
        {"Mutant": "M03", "Category": "Decision-rule", "EP": 1, "BVA": 1, "DTT": 0, "Valid": 1},
    ]
    metrics = calculate_metrics(rows, {"EP": 2, "BVA": 4, "DTT": 2})
    assert metrics["suites"]["EP"]["ddr_percent"] == 66.67
    assert metrics["suites"]["EP"]["efficiency"] == 1.0
    assert metrics["overlap"]["EP-BVA"]["mutants"] == ["M03"]
    assert metrics["unique"]["DTT"]["count"] == 0
    assert metrics["combined"]["ddr_percent"] == 100.0
