from pathlib import Path

from book_parser import parse_book
from journal_parser import parse_journal_article
from newspaper_parser import parse_newspaper_article
from report_parser import parse_report
from web_article_parser import parse_web_article

def parse_file(file_path: str) -> dict:
    """
    Unified parser that dispatches based on top-level folder.
    Returns a dict with keys: page_content, metadata.
    """
    path = Path(file_path)
    try:
        folder = path.parts[1]  # e.g., "journals" from "amatol/journals/..."
    except IndexError:
        raise ValueError(f"Unexpected file structure: {file_path}")

    if folder == "books":
        return parse_book(file_path)
    elif folder == "journals":
        return parse_journal_article(file_path)
    elif folder == "newspapers":
        return parse_newspaper_article(file_path)
    elif folder == "reports":
        return parse_report(file_path)
    elif folder == "web_articles":
        return parse_web_article(file_path)
    else:
        raise ValueError(f"Unknown source type: {folder} for file {file_path}")

if __name__ == "__main__":
    root = Path("amatol")
    all_files = root.rglob("*.txt")

    for file_path in all_files:
        parsed = parse_web_article(file_path)
        print("\n=== File:", file_path, "===")
        print("Page Content:\n", parsed["page_content"], sep="")
        print("\nMetadata:")
        for k, v in parsed["metadata"].items():
            print(f"  {k}: {v}")
