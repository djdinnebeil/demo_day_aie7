import json
from pathlib import Path

# Load metadata.json if available
META_FILE = Path("amatol/journals/metadata.json")
if META_FILE.exists():
    with open(META_FILE, "r", encoding="utf-8") as f:
        JOURNAL_META = json.load(f).get("journals", {})
else:
    JOURNAL_META = {}

def format_page_label(pages: str) -> str:
    """Format page label with p. or pp. depending on single vs. range."""
    if not pages:
        return None
    if "-" in pages:  # e.g., "45-54"
        return f"pp. {pages.replace('-', '–')}"  # en-dash for ranges
    else:
        return f"p. {pages}"

def parse_journal_article(file_path: str) -> dict:
    """Parse a journal article into structured output."""
    path = Path(file_path)
    fname = path.stem

    entry = JOURNAL_META.get(fname, {})
    raw_text = path.read_text(encoding="utf-8").strip()

    source_id = fname
    source_name = entry.get("journal", source_id.title())

    # Format pages nicely
    pages = entry.get("pages")
    page_label = format_page_label(pages) if pages else None

    # Build citation
    citation = entry.get("citation")
    if not citation:
        vol = entry.get("volume")
        issue = entry.get("issue")
        season = entry.get("season")
        title = entry.get("title", fname)

        if vol and issue and season and page_label:
            citation = f"{source_name} {vol}.{issue}, {season}, {page_label}, \"{title}\""
        elif vol and issue and page_label:
            citation = f"{source_name} {vol}.{issue}, {page_label}, \"{title}\""
        else:
            citation = f"{source_name}, \"{title}\""

    return {
        "page_content": raw_text,
        "metadata": {
            "source_type": "journal",
            "source_id": source_id,
            "source_name": source_name,
            "journal": entry.get("journal"),
            "volume": entry.get("volume"),
            "issue": entry.get("issue"),
            "season": entry.get("season"),
            "pages": pages,
            "title": entry.get("title", fname),
            "file_path": str(file_path),
            "citation": citation
        }
    }

# Example usage
if __name__ == "__main__":
    test_file = "amatol/journals/2019-02-15__sojourn__p45-54__all-aboard-for-amatol-new-jersey.txt"
    parsed = parse_journal_article(test_file)
    print(parsed["metadata"])
