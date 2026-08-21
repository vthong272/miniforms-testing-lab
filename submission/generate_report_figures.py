"""Generate vector PDF figures from the frozen MiniForms metrics."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "experiment-results" / "frozen-v1.0-run-20260814" / "metrics.json"
OUTPUT_DIR = ROOT / "submission" / "overleaf-report" / "figures"
COLORS = {"EP": "#2463eb", "BVA": "#10b981", "DTT": "#f59e0b", "Combined": "#334155"}
WIDTH, HEIGHT = 660, 292


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Report", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Report-Bold", r"C:\Windows\Fonts\arialbd.ttf"))


def draw_axes(pdf: canvas.Canvas, left: float, bottom: float, width: float, height: float,
              maximum: float, ticks: list[float], label: str) -> None:
    pdf.setStrokeColor(HexColor("#94a3b8"))
    pdf.setLineWidth(0.7)
    pdf.line(left, bottom, left, bottom + height)
    pdf.line(left, bottom, left + width, bottom)
    pdf.setFont("Report", 8)
    for tick in ticks:
        y = bottom + height * tick / maximum
        pdf.setStrokeColor(HexColor("#e2e8f0"))
        pdf.line(left, y, left + width, y)
        pdf.setFillColor(HexColor("#475569"))
        pdf.drawRightString(left - 6, y - 3, f"{tick:g}")
    pdf.saveState()
    pdf.translate(13, bottom + height / 2)
    pdf.rotate(90)
    pdf.setFillColor(HexColor("#334155"))
    pdf.setFont("Report", 9)
    pdf.drawCentredString(0, 0, label)
    pdf.restoreState()


def draw_bars(pdf: canvas.Canvas, values: list[float], labels: list[str], colors: list[str],
              left: float, bottom: float, width: float, height: float, maximum: float,
              value_format, bar_width_ratio: float = 0.58) -> None:
    slot = width / len(values)
    bar_width = slot * bar_width_ratio
    for index, (value, label, color) in enumerate(zip(values, labels, colors)):
        x = left + index * slot + (slot - bar_width) / 2
        bar_height = height * value / maximum
        pdf.setFillColor(HexColor(color))
        pdf.roundRect(x, bottom, bar_width, bar_height, 2.5, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#0f172a"))
        pdf.setFont("Report-Bold", 8.5)
        pdf.drawCentredString(x + bar_width / 2, bottom + bar_height + 7, value_format(value))
        pdf.setFont("Report", 8.5)
        pdf.drawCentredString(x + bar_width / 2, bottom - 14, label)


def title(pdf: canvas.Canvas, text: str) -> None:
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Report-Bold", 13)
    pdf.drawCentredString(WIDTH / 2, HEIGHT - 25, text)


def overall_figure(metrics: dict) -> None:
    pdf = canvas.Canvas(str(OUTPUT_DIR / "overall_metrics.pdf"), pagesize=(WIDTH, HEIGHT))
    suites = ["EP", "BVA", "DTT"]
    colors = [COLORS[suite] for suite in suites]
    ddr = [metrics["suites"][suite]["ddr_percent"] for suite in suites]
    efficiency = [metrics["suites"][suite]["efficiency"] for suite in suites]
    title(pdf, "DDR tổng thể và hiệu quả trên mỗi test case")
    panels = [(42, 58, 270, 170), (370, 58, 250, 170)]
    draw_axes(pdf, *panels[0], maximum=60, ticks=[0, 20, 40, 60], label="DDR (%)")
    draw_bars(pdf, ddr, suites, colors, *panels[0], maximum=60,
              value_format=lambda value: f"{value:.2f}%")
    draw_axes(pdf, *panels[1], maximum=0.36, ticks=[0, 0.1, 0.2, 0.3], label="Efficiency")
    draw_bars(pdf, efficiency, suites, colors, *panels[1], maximum=0.36,
              value_format=lambda value: f"{value:.4f}")
    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Report", 8)
    pdf.drawCentredString(177, 38, "Defect Detection Rate")
    pdf.drawCentredString(495, 38, "Mutant phát hiện / test case")
    pdf.save()


def category_figure(metrics: dict) -> None:
    pdf = canvas.Canvas(str(OUTPUT_DIR / "category_ddr.pdf"), pagesize=(WIDTH, HEIGHT))
    title(pdf, "Defect Detection Rate theo loại lỗi")
    left, bottom, chart_width, chart_height = 55, 60, 565, 170
    draw_axes(pdf, left, bottom, chart_width, chart_height, 100, [0, 25, 50, 75, 100], "DDR (%)")
    categories = ["Partition", "Boundary", "Decision-rule"]
    category_labels = ["Lỗi phân vùng", "Lỗi biên", "Lỗi luật quyết định"]
    suites = ["EP", "BVA", "DTT"]
    group_width = chart_width / 3
    bar_width = 42
    gap = 5
    for category_index, (category, category_label) in enumerate(zip(categories, category_labels)):
        group_left = left + category_index * group_width
        total_width = 3 * bar_width + 2 * gap
        start = group_left + (group_width - total_width) / 2
        for suite_index, suite in enumerate(suites):
            value = metrics["suites"][suite]["by_category"][category]["ddr_percent"]
            x = start + suite_index * (bar_width + gap)
            bar_height = chart_height * value / 100
            pdf.setFillColor(HexColor(COLORS[suite]))
            if value > 0:
                pdf.roundRect(x, bottom, bar_width, bar_height, 2.5, stroke=0, fill=1)
            pdf.setFillColor(HexColor("#0f172a"))
            pdf.setFont("Report-Bold", 7.5)
            pdf.drawCentredString(x + bar_width / 2, bottom + bar_height + 6, f"{value:.0f}%")
        pdf.setFont("Report", 8.5)
        pdf.drawCentredString(group_left + group_width / 2, bottom - 16, category_label)
    legend_x = 235
    for index, suite in enumerate(suites):
        x = legend_x + index * 78
        pdf.setFillColor(HexColor(COLORS[suite]))
        pdf.rect(x, 25, 10, 10, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#334155"))
        pdf.setFont("Report", 8.5)
        pdf.drawString(x + 14, 26, suite)
    pdf.save()


def unique_figure(metrics: dict) -> None:
    pdf = canvas.Canvas(str(OUTPUT_DIR / "unique_combined.pdf"), pagesize=(WIDTH, HEIGHT))
    title(pdf, "Unique kills và hiệu quả kết hợp")
    labels = ["Chỉ EP", "Chỉ BVA", "Chỉ DTT", "Kết hợp"]
    values = [metrics["unique"]["EP"]["count"], metrics["unique"]["BVA"]["count"],
              metrics["unique"]["DTT"]["count"], metrics["combined"]["killed"]]
    colors = [COLORS["EP"], COLORS["BVA"], COLORS["DTT"], COLORS["Combined"]]
    left, bottom, chart_width, chart_height = 58, 58, 555, 174
    draw_axes(pdf, left, bottom, chart_width, chart_height, 18, [0, 3, 6, 9, 12, 15, 18], "Số mutant")
    draw_bars(pdf, values, labels, colors, left, bottom, chart_width, chart_height, 18,
              value_format=lambda value: str(int(value)), bar_width_ratio=0.52)
    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Report", 8)
    pdf.drawCentredString(WIDTH / 2, 25, "Hợp ba suite phát hiện 18/18 mutant (DDR 100%)")
    pdf.save()


def main() -> None:
    register_fonts()
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    overall_figure(metrics)
    category_figure(metrics)
    unique_figure(metrics)


if __name__ == "__main__":
    main()
