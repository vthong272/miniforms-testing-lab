"""Static validation for the Overleaf submission package."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "overleaf-report"
TEX = REPORT / "main.tex"
BIB = REPORT / "references.bib"


def fail(message: str) -> None:
    raise SystemExit(f"FAILED: {message}")


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    bib = BIB.read_text(encoding="utf-8")

    for required in ["llncs.cls", "splncs04.bst", "references.bib", "README_OVERLEAF.md"]:
        if not (REPORT / required).is_file():
            fail(f"missing {required}")

    begins = re.findall(r"\\begin\{([^}]+)\}", text)
    ends = re.findall(r"\\end\{([^}]+)\}", text)
    if begins != list(reversed(list(reversed(ends)))):
        if sorted(begins) != sorted(ends):
            fail("LaTeX environments are unbalanced")

    labels = re.findall(r"\\label\{([^}]+)\}", text)
    if len(labels) != len(set(labels)):
        fail("duplicate LaTeX label")

    citations = set()
    for group in re.findall(r"\\cite\{([^}]+)\}", text):
        citations.update(key.strip() for key in group.split(","))
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    missing_citations = sorted(citations - bib_keys)
    if missing_citations:
        fail(f"missing BibTeX entries: {missing_citations}")

    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    for relative in figures:
        path = REPORT / relative
        if not path.is_file():
            fail(f"missing figure: {relative}")
        reader = PdfReader(str(path))
        if len(reader.pages) != 1:
            fail(f"figure is not a one-page PDF: {relative}")

    required_facts = ["30/30", "51/51", "29/29", "55,56\\%", "50,00\\%", "38,89\\%", "18/18"]
    for fact in required_facts:
        if fact not in text:
            fail(f"missing frozen result: {fact}")

    print(f"PASS: {len(citations)} citations, {len(labels)} labels, {len(figures)} vector figures")


if __name__ == "__main__":
    main()
