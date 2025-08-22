import re
import json
from pathlib import Path

# Load metadata.json once at startup
with open("amatol/newspapers/metadata.json", "r", encoding="utf-8") as f:
    NEWSPAPER_METADATA = json.load(f)

def parse_newspaper_article(file_path: str) -> dict:
    """Parse a newspaper text file into chunk text + minimal useful metadata."""

    # --- Step 1: Read + normalize line endings ---
    raw_text = Path(file_path).read_text(encoding="utf-8")
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # --- Step 2: Split into header vs body ---
    parts = re.split(r"\n\s*\n", text, maxsplit=1)
    header = parts[0].strip()
    body = parts[1].strip() if len(parts) > 1 else ""

    # --- Step 3: Extract filename metadata ---
    # ex: 1919-12-18__philadelphia-inquirer__p5__auction-at-amatol.txt
    fname = Path(file_path).stem
    parts = fname.split("__")
    date_str = parts[0]               # e.g., 1919-12-18
    newspaper = parts[1].replace("-", " ").title()  # e.g., Philadelphia Inquirer
    page = parts[2]                   # e.g., p5

    # --- Step 4: Load attribution patterns for this newspaper ---
    patterns = NEWSPAPER_METADATA.get(newspaper, {}).get("attribution_patterns", [])
    if not patterns:
        patterns = NEWSPAPER_METADATA["default"]["attribution_patterns"]

    # --- Step 5: Parse header (title, subtitles, attribution, city_date) ---
    header_lines = [l.strip() for l in header.split("\n") if l.strip()]

    title = header_lines[0].title()
    city_date = header_lines[-1] if len(header_lines) > 1 else None
    middle_lines = header_lines[1:-1]  # all between title and city_date

    subtitles, attribution = [], None
    for line in middle_lines:
        line_norm = line.lower()
        if any(line_norm.startswith(pat) for pat in patterns):
            attribution = line
        else:
            subtitles.append(line)


    # --- Step 6: Build citation ---
    citation_title = title.title()
    if subtitles:
        citation_title += ": " + "; ".join(subtitles)

    citation = f'{newspaper}, {date_str}, {page}, "{citation_title}"'

    # --- Step 7: Build chunk text ---
    chunk_parts = [title]
    if subtitles:
        chunk_parts.extend(subtitles)
    chunk_parts.append(body)
    page_content = "\n".join([p for p in chunk_parts if p.strip()])

    # --- Step 8: Return structured output ---
    return {
        "page_content": page_content,
        "metadata": {
            "source_type": "newspaper",
            "newspaper": newspaper,
            "date": date_str,
            "page": page,
            "title": title,
            "subtitles": subtitles,
            "attribution": attribution,
            "city_date": city_date,
            "file_path": str(file_path),
            "citation": citation
        }
    }

# --- Run through all newspaper text files ---
if __name__ == "__main__":
    root = Path("amatol/newspapers")
    all_files = root.rglob("*.txt")

    for file_path in all_files:
        parsed = parse_newspaper_article(file_path)
        print("\n=== File:", file_path, "===")
        print("Page Content:\n", parsed["page_content"], sep="")
        print("\nMetadata:")
        for k, v in parsed["metadata"].items():
            print(f"  {k}: {v}")
