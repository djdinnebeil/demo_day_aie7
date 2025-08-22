import json
from pathlib import Path

def format_page_label(page: str) -> str:
    """Format page label with p. or pp. depending on single vs. range."""
    if "-" in page:  # e.g., p135-136
        pages = page.lstrip("p")
        return f"pp. {pages.replace('-', '–')}"  # en-dash for ranges
    else:
        pages = page.lstrip("p")
        return f"p. {pages}"

def parse_book(file_path: str) -> dict:
    """Parse a book text file into structured output."""
    path = Path(file_path)
    fname = path.stem  # filename without .txt
    folder = path.parent
    source_id = folder.name

    # Look for metadata.json in the same folder
    meta_file = folder / "metadata.json"
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # If metadata.json has multiple entries, look up by filename
        if isinstance(data, dict) and "books" in data:
            entry = data["books"].get(fname, {})
        else:
            # Assume metadata.json just describes this one book
            entry = data
    else:
        entry = {}

    raw_text = path.read_text(encoding="utf-8").strip()

    # Extract metadata fields
    source_name = entry.get("title", source_id.replace("_", " ").title())
    year = entry.get("year")
    pages = entry.get("pages") or fname
    page_label = format_page_label(pages) if pages.startswith("p") else pages

    # Build citation
    citation = entry.get("citation")
    if not citation:
        if year:
            citation = f"{source_name}, {year}, {page_label}"
        else:
            citation = f"{source_name}, {page_label}"

    return {
        "page_content": raw_text,
        "metadata": {
            "source_type": "book",
            "source_id": source_id,
            "source_name": source_name,
            "title": entry.get("title", source_name),
            "author": entry.get("author"),
            "year": year,
            "pages": pages,
            "file_path": str(file_path),
            "citation": citation
        }
    }

# Example usage
if __name__ == "__main__":
    test_file = "amatol/books/amatol_book/p135-136.txt"
    parsed = parse_book(test_file)
    print(parsed["metadata"])
