from pathlib import Path
import re

def extract_date_from_text_or_filename(fname: str, text: str) -> str | None:
    """Try to find a date in the filename or content (YYYY-MM-DD)."""
    match = re.search(r"\d{4}-\d{2}-\d{2}", fname)
    if match:
        return match.group(0)
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    if match:
        return match.group(0)
    return None

def slug_to_title(slug: str) -> str:
    """Convert filename or slug to human-readable title."""
    return slug.replace("_", " ").replace("-", " ").title()

def parse_unsorted(file_path: str) -> dict:
    """Parse a loosely formatted document into structured output."""
    path = Path(file_path)
    fname = path.stem

    raw_text = path.read_text(encoding="utf-8").strip()

    # Try to guess a date
    date = extract_date_from_text_or_filename(fname, raw_text)

    # Build fallback citation
    citation = f'Unsorted Document: {slug_to_title(fname)}'
    if date:
        citation += f" ({date})"

    return {
        "page_content": raw_text,
        "metadata": {
            "source_type": "unsorted",
            "source_id": fname,
            "title": slug_to_title(fname),
            "date": date,
            "file_path": str(file_path),
            "citation": citation,
        }
    }

if __name__ == "__main__":
    test_file = "./unsorted/The Greenwich Tea Party How it has been Remembered.txt"
    parsed = parse_unsorted(test_file)
    print(parsed)
