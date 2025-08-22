import json
import re
from pathlib import Path

# Load metadata.json
with open("amatol/journals/metadata.json", "r", encoding="utf-8") as f:
    METADATA = json.load(f)

def parse_article(file_path: str) -> dict:
    """Parse newspaper or journal text file into structured output."""
    fname = Path(file_path).stem 

    # --- Case 1: Journal ---
    if fname in METADATA.get("journals", {}):
        entry = METADATA["journals"][fname]
        raw_text = Path(file_path).read_text(encoding="utf-8").strip()

        return {
            "page_content": raw_text,  # whole text body
            "metadata": {
                "source_type": "journal",
                "journal": entry["journal"],
                "volume": entry["volume"],
                "issue": entry["issue"],
                "season": entry["season"],
                "pages": entry["pages"],
                "title": entry["title"],
                "file_path": str(file_path),
                "citation": entry["citation"]
            }
        }

    # --- Case 2: Newspaper (reuse your existing logic) ---
    # For brevity I’ll just note: you’d call parse_newspaper_article(file_path)
    # and return its result here.
    else:
        from newspaper_parser import parse_newspaper_article
        return parse_newspaper_article(file_path)

# --- Run through all newspaper text files ---
if __name__ == "__main__":
    root = Path("amatol/journals")
    all_files = root.rglob("*.txt")

    for file_path in all_files:
        parsed = parse_article(file_path)
        print("\n=== File:", file_path, "===")
        print("Page Content:\n", parsed["page_content"], sep="")
        print("\nMetadata:")
        for k, v in parsed["metadata"].items():
            print(f"  {k}: {v}")
