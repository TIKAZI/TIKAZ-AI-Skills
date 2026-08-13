#!/usr/bin/env python3
"""Convert generated PDFs page-by-page and publish literal fidelity metrics."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter


def convert_page(converter: Path, page_pdf: Path, output_md: Path) -> None:
    completed = subprocess.run(
        [str(converter), str(page_pdf), "-o", str(output_md)],
        check=False, capture_output=True, text=True,
    )
    if completed.returncode != 0 or not output_md.is_file():
        raise RuntimeError(f"converter failed for {page_pdf.name}: {completed.stderr.strip()}")


def convert_page_pdfplumber(page_pdf: Path, output_md: Path) -> None:
    """Extract literal text and tables with the installed pdfplumber adapter."""
    blocks = []
    with pdfplumber.open(page_pdf) as document:
        page = document.pages[0]
        text = (page.extract_text() or "").strip()
        if text:
            blocks.append(text)
        for table in page.extract_tables() or []:
            rows = [["" if cell is None else str(cell).replace("\n", " ") for cell in row] for row in table]
            if not rows:
                continue
            width = max(len(row) for row in rows)
            rows = [row + [""] * (width - len(row)) for row in rows]
            blocks.append("| " + " | ".join(rows[0]) + " |")
            blocks.append("| " + " | ".join(["---"] * width) + " |")
            blocks.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    output_md.write_text("\n\n".join(blocks).strip() + "\n", encoding="utf-8", newline="\n")


def score(expected: dict, markdown: str) -> dict:
    categories = {name: [str(value) for value in expected.get(name, [])] for name in ("required_text", "numeric_facts", "table_cells")}
    missing = {name: [value for value in values if value not in markdown] for name, values in categories.items()}
    pages = int(expected["pages"])
    page_anchors = [f"<!-- page: {page} -->" for page in range(1, pages + 1)]
    missing["page_anchors"] = [str(page) for page, anchor in enumerate(page_anchors, 1) if anchor not in markdown]
    def recall(name):
        return 1.0 if not categories[name] else round((len(categories[name]) - len(missing[name])) / len(categories[name]), 4)
    return {
        "id": expected["id"], "required_text_recall": recall("required_text"),
        "numeric_fact_recall": recall("numeric_facts"), "table_cell_recall": recall("table_cells"),
        "page_anchor_coverage": round((pages - len(missing["page_anchors"])) / pages, 4),
        "missing": missing, "visual_claim_scored": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", choices=("markitdown", "pdfplumber"), default="markitdown")
    parser.add_argument("--converter", type=Path)
    parser.add_argument("--ground-truth", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    converter = args.converter.resolve() if args.converter else None
    if args.adapter == "markitdown" and converter is None:
        parser.error("--converter is required for the markitdown adapter")
    truth_file = args.ground_truth.resolve()
    truth = json.loads(truth_file.read_text(encoding="utf-8"))
    output = args.output.resolve()
    converted = output / "converted"
    converted.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        for document in truth["documents"]:
            pdf = (truth_file.parent / document["pdf"]).resolve()
            reader = PdfReader(str(pdf))
            parts = []
            for page_number, page in enumerate(reader.pages, 1):
                writer = PdfWriter()
                writer.add_page(page)
                page_pdf = temp / f"{document['id']}-page-{page_number}.pdf"
                page_md = temp / f"{document['id']}-page-{page_number}.md"
                with page_pdf.open("wb") as stream:
                    writer.write(stream)
                if args.adapter == "pdfplumber":
                    convert_page_pdfplumber(page_pdf, page_md)
                else:
                    convert_page(converter, page_pdf, page_md)
                parts.append(f"<!-- page: {page_number} -->\n\n{page_md.read_text(encoding='utf-8').strip()}\n")
            markdown = "\n".join(parts)
            (converted / f"{document['id']}.md").write_text(markdown, encoding="utf-8", newline="\n")
            results.append(score(document, markdown))
    def aggregate(field):
        values = [float(item[field]) for item in results]
        return round(sum(values) / len(values), 4)
    summary = {
        "schema_version": 1, "adapter": args.adapter,
        "converter": str(converter) if converter else "installed pdfplumber",
        "documents": len(results), "results": results,
        "required_text_recall": aggregate("required_text_recall"),
        "numeric_fact_recall": aggregate("numeric_fact_recall"),
        "table_cell_recall": aggregate("table_cell_recall"),
        "page_anchor_coverage": aggregate("page_anchor_coverage"),
        "visual_description_accuracy": None,
        "claim_boundary": "Generated text/table PDFs; literal recall only. Visual description remains pending.",
    }
    (output / "metrics.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
