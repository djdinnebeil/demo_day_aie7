import json
from pathlib import Path

def load_folder_metadata(folder: Path) -> dict:
    """Load metadata.json from a folder if available."""
    meta_file = folder / "metadata.json"
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def format_source_name(source_id: str) -> str:
    """Convert machine id into human-friendly name."""
    return source_id.replace('_', ' ').title()

def format_page_label(page: str) -> str:
    """Format page label with p. or pp. depending on single vs. range."""
    if "-" in page:  # e.g., p135-136
        # strip the "p" prefix and reformat
        pages = page.lstrip("p")
        return f"pp. {pages.replace('-', '–')}"  # en-dash for ranges
    else:
        pages = page.lstrip("p")
        return f"p. {pages}"

def extract_books_metadata(root_dir: str = "amatol/books"):
    book_paths = Path(root_dir).rglob("*.txt")
    metadata_list = []

    for path in book_paths:
        folder = path.parent
        source_id = folder.name  
        folder_meta = load_folder_metadata(folder)
        
        source_name = folder_meta.get("title", format_source_name(source_id))
        year = folder_meta.get("year", None)
        page = path.stem  # e.g., "p007" or "p135-136"
        page_label = format_page_label(page)

        if year:
            citation = f"{source_name}, {year}, {page_label}"
        else:
            citation = f"{source_name}, {page_label}"
        
        meta = {
            "source_type": "book",
            "source_id": source_id,
            "source_name": source_name,
            "year": year,
            "page": page,
            "file_path": str(path),
            "citation": citation
        }
        metadata_list.append(meta)

    return metadata_list


if __name__ == "__main__":
    books_metadata = extract_books_metadata()
    for m in books_metadata:
        print(m)
