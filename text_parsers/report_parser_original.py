import json
from pathlib import Path

# --- Load metadata.json once at startup ---
META_FILE = Path("amatol/reports/metadata.json")
if META_FILE.exists():
    with open(META_FILE, "r", encoding="utf-8") as f:
        REPORT_METADATA = json.load(f).get("reports", {})
else:
    REPORT_METADATA = {}


def parse_report(file_path: str) -> dict:
    """Parse a report text file into structured metadata + text."""

    path = Path(file_path)
    report_id = path.stem  # filename without .txt
    raw_text = path.read_text(encoding="utf-8").strip()

    # Lookup metadata if available
    meta = REPORT_METADATA.get(report_id, {})

    # Default citation if metadata.json missing
    citation = meta.get("citation", f"Report, {report_id}")

    return {
        "page_content": raw_text,
        "metadata": {
            "source_type": "report",
            "report_id": report_id,
            "file_path": str(path),
            "title": meta.get("title"),
            "coverage_years": meta.get("coverage_years"),
            "publication_year": meta.get("publication_year"),
            "pages": meta.get("pages"),
            "citation": citation,
        }
    }


def parse_all_reports(root_dir: str = "amatol/reports"):
    """Parse all .txt reports in the folder."""
    report_paths = Path(root_dir).rglob("*.txt")
    parsed = [parse_report(str(p)) for p in report_paths]
    return parsed


if __name__ == "__main__":
    reports = parse_all_reports()
    for r in reports:
        print(json.dumps(r["metadata"], indent=2))
