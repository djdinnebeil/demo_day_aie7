from pathlib import Path

from text_parsers.book_parser import parse_book
from text_parsers.journal_parser import parse_journal_article
from text_parsers.newspaper_parser import parse_newspaper_article
from text_parsers.report_parser import parse_report
from text_parsers.web_article_parser import parse_web_article

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


    # if folder == "books":
    #     return parse_book(file_path)
    # else:
    #     return {"page_content": "", "metadata": {}}


    # if folder == "journals":
    #     return parse_journal_article(file_path)
    # else:
    #     return {"page_content": "", "metadata": {}}


    # if folder == "newspapers":
    #     return parse_newspaper_article(file_path)
    # else:
    #     return {"page_content": "", "metadata": {}}

    # if folder == "reports":
    #     return parse_report(file_path)
    # else:
    #     return {"page_content": "", "metadata": {}}

    # if folder == "web_articles":
    #     return parse_web_article(file_path)
    # else:
    #     return {"page_content": "", "metadata": {}}



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

    with open('amatol_parsed.txt', 'w') as f:
        for file_path in all_files:
            parsed = parse_file(file_path)
            print("\n=== File:", file_path, "===", file=f)
            print("Page Content:\n", parsed["page_content"], sep="", file=f)
            print("\nMetadata:", file=f)
            for k, v in parsed["metadata"].items():
                print(f"  {k}: {v}", file=f)
