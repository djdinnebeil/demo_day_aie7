import json
from pathlib import Path

# Load metadata.json if available
META_FILE = Path("amatol/web_articles/metadata.json")
if META_FILE.exists():
    with open(META_FILE, "r", encoding="utf-8") as f:
        WEB_META = json.load(f).get("web_articles", {})
else:
    WEB_META = {}

def parse_web_article(file_path: str) -> dict:
    """Parse a web article into structured output."""
    path = Path(file_path)
    fname = path.stem  # no .txt

    # ex: 2011-06-11__lost-history__brief-history-of-amatol-nj
    parts = fname.split("__")
    date_str = parts[0]
    source_id = parts[1]  # e.g., "lost-history"
    slug = parts[2] if len(parts) > 2 else None

    # Look up a cleaner source name if available
    source_name = WEB_META.get(source_id, {}).get("source", source_id.replace("-", " ").title())

    # Read the body text
    raw_text = path.read_text(encoding="utf-8").strip()

    # Build citation
    citation_title = slug.replace("-", " ").title() if slug else "Untitled"
    citation = f'{source_name}, {date_str}, "{citation_title}"'

    return {
        "page_content": raw_text,
        "metadata": {
            "source_type": "web_article",
            "source_id": source_id,
            "source": source_name,
            "date": date_str,
            "slug": slug,
            "file_path": str(file_path),
            "citation": citation
        }
    }

# --- Run through all web article text files ---
if __name__ == "__main__":
    root = Path("amatol/web_articles")
    all_files = root.rglob("*.txt")

    for file_path in all_files:
        parsed = parse_web_article(file_path)
        print("\n=== File:", file_path, "===")
        print("Page Content:\n", parsed["page_content"], sep="")
        print("\nMetadata:")
        for k, v in parsed["metadata"].items():
            print(f"  {k}: {v}")
