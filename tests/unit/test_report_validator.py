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


def test_title_block_matches_the_english_template_without_duplicate_affiliation():
    report_main = Path(__file__).resolve().parents[2] / "submission" / "overleaf-report" / "main.tex"
    text = report_main.read_text(encoding="utf-8")

    assert "lớp 3W" not in text
    assert "lớp SE2036" not in text
    assert "Giảng viên hướng dẫn" not in text
    assert text.count(r"\institute{") == 1
    assert text.count("FPT University, Ho Chi Minh City, Vietnam") == 1
    assert text.count("thongvinh2@gmail.com") == 1
    assert text.count("daothingoctram0604@gmail.com") == 1
    assert text.count("thanhthao725218@gmail.com") == 1
