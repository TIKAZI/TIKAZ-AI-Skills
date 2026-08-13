#!/usr/bin/env python3
"""Generate TIKAZ-owned PDF fidelity fixtures from declared ground truth."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "fixtures"


def build_text_report() -> None:
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Quarterly Operations Report", styles["Title"]),
        Spacer(1, 18),
        Paragraph("Version 8.2.1 passed 42 checks. Operating margin reached 24.6%.", styles["BodyText"]),
        PageBreak(),
        Paragraph("Release Decision", styles["Heading1"]),
        Paragraph("All checks passed. Rollback window remains 30 minutes.", styles["BodyText"]),
    ]
    SimpleDocTemplate(str(OUTPUT / "text-report.pdf"), pagesize=A4).build(story)


def build_table_report() -> None:
    styles = getSampleStyleSheet()
    data = [
        ["Region", "Capacity", "Utilization"],
        ["East", "120", "88.5%"],
        ["West", "95", "76.0%"],
    ]
    table = Table(data, colWidths=[150, 120, 120])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4C1D95")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.75, colors.HexColor("#6B7280")),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("PADDING", (0, 0), (-1, -1), 9),
    ]))
    story = [
        Paragraph("Regional Capacity Table", styles["Title"]), Spacer(1, 18), table, Spacer(1, 16),
        Paragraph("Capacity is measured in pallets per hour.", styles["BodyText"]),
    ]
    SimpleDocTemplate(str(OUTPUT / "table-report.pdf"), pagesize=A4).build(story)


def build_illustrated_report() -> None:
    styles = getSampleStyleSheet()
    flow = Table(
        [["Inbound", "->", "Inspection", "->", "Storage"]],
        colWidths=[105, 35, 105, 35, 105], rowHeights=[70],
    )
    flow.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#DBEAFE")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#EDE9FE")),
        ("BACKGROUND", (4, 0), (4, 0), colors.HexColor("#D1FAE5")),
        ("BOX", (0, 0), (0, 0), 1.2, colors.HexColor("#2563EB")),
        ("BOX", (2, 0), (2, 0), 1.2, colors.HexColor("#7C3AED")),
        ("BOX", (4, 0), (4, 0), 1.2, colors.HexColor("#059669")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
    ]))
    story = [
        Paragraph("Warehouse Flow Diagram", styles["Title"]), Spacer(1, 30), flow, Spacer(1, 20),
        Paragraph("3 stages are reviewed every 12 hours.", styles["BodyText"]),
    ]
    SimpleDocTemplate(str(OUTPUT / "illustrated-report.pdf"), pagesize=A4).build(story)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_text_report()
    build_table_report()
    build_illustrated_report()
    print(f"Generated 3 PDF fixtures in {OUTPUT}")


if __name__ == "__main__":
    main()
