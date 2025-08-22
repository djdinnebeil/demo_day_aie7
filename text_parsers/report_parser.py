import json
from pathlib import Path

# Load metadata.json once at startup
META_FILE = Path("amatol/reports/metadata.json")
if META_FILE.exists():
    with open(META_FILE, "r", encoding="utf-8") as f:
        REPORT_META = json.load(f).get("reports", {})
else:
    REPORT_META = {}


def parse_report(file_path: str) -> dict:
    """Parse a report text file into structured output."""
    path = Path(file_path)
    fname = path.stem  # filename without .txt

    # Look up metadata entry for this report
    entry = REPORT_META.get(fname, {})

    raw_text = path.read_text(encoding="utf-8").strip()

    # Build citation fallback if missing
    citation = entry.get("citation")
    if not citation:
        citation = f'Report, {fname}'

    return {
        "page_content": raw_text,
        "metadata": {
            "source_type": "report",
            "source_id": fname,  # machine-friendly key (like source_id in other parsers)
            "title": entry.get("title"),
            "coverage_years": entry.get("coverage_years"),
            "publication_year": entry.get("publication_year"),
            "pages": entry.get("pages"),
            "file_path": str(file_path),
            "citation": citation
        }
    }


def parse_all_reports(root_dir: str = "amatol/reports") -> list[dict]:
    """Parse all report files under the given directory."""
    report_paths = Path(root_dir).rglob("*.txt")
    results = []
    for file_path in report_paths:
        results.append(parse_report(file_path))
    return results


# Example usage
if __name__ == "__main__":
    reports = parse_all_reports()
    for r in reports:
        print("\n=== File:", r["metadata"]["file_path"], "===")
        print("Metadata:", r["metadata"])
        print("Preview text:", r["page_content"][:200], "...")
