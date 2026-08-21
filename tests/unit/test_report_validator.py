from pathlib import Path

import pytest

from submission.validate_report import validate_tex_document


def test_rejects_truncated_latex_body_without_document_environment(tmp_path):
    truncated = tmp_path / "main.tex"
    truncated.write_text(
        "\\documentclass[runningheads]{llncs}\n"
        "EP, BVA và DTT là ba kỹ thuật hộp đen phổ biến.\n"
        "\\section{Phương pháp nghiên cứu}\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=r"begin\{document\}"):
        validate_tex_document(truncated)


def test_accepts_complete_overleaf_main():
    report_main = Path(__file__).resolve().parents[2] / "submission" / "overleaf-report" / "main.tex"

    validate_tex_document(report_main)
