import sys
from pathlib import Path
import fitz  # PyMuPDF

def pdf_to_txt(pdf_path: str, txt_path: str | None = None) -> str:
    """
    Convert a PDF file to plain text.
    If txt_path is provided, saves output to that file.
    Returns the extracted text as a string.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Default output path: same name, but with .txt
    if txt_path is None:
        txt_path = pdf_path.with_suffix(".txt")
    else:
        txt_path = Path(txt_path)

    doc = fitz.open(pdf_path)
    text_chunks = []
    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text("text")
        text_chunks.append(page_text.strip())
    text = "\n\n".join(text_chunks).strip()

    txt_path.write_text(text, encoding="utf-8")
    print(f"Saved text to {txt_path}")
    return text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_txt.py input.pdf [output.txt]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    txt_file = sys.argv[2] if len(sys.argv) > 2 else None
    pdf_to_txt(pdf_file, txt_file)
