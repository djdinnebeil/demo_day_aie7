from pathlib import Path

import re

# List of "small words" that should usually be lowercase in title case
SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for",
               "if", "in", "nor", "of", "on", "or", "per", "so",
               "the", "to", "up", "via", "yet"}

def normalize_title(title: str) -> str:
    title = title.strip()

    # If whole line is uppercase, normalize it
    if title.isupper():
        words = title.lower().split()
        fixed = []
        for i, w in enumerate(words):
            # Keep acronyms/numbers in ALLCAPS if length <= 3
            if len(w) <= 3 and w.isupper():
                fixed.append(w)
            elif i == 0 or i == len(words) - 1:  # Always capitalize first/last word
                fixed.append(w.capitalize())
            elif w in SMALL_WORDS:
                fixed.append(w)  # small words stay lowercase
            else:
                fixed.append(w.capitalize())
        return " ".join(fixed)

    return title

def process_newspapers(root_dir: str = "amatol/newspapers"):
    root = Path(root_dir)
    if not root.exists():
        print(f"Path not found: {root_dir}")
        return
    
    results = []
    
    for path in sorted(root.rglob("*.txt")):
        # Example filename:
        # 1918-02-08__trenton-evening-times__p1__cannot-be-built-by-camp-dix.txt
        parts = path.stem.split("__")
        if len(parts) < 3:
            continue  # skip unexpected filenames

        date = parts[0]  # e.g. "1918-02-08"
        source_id = parts[1]  # e.g. "trenton-evening-times"
        page = parts[2]  # e.g. "p1"

        # Read first line as title
        with path.open(encoding="utf-8", errors="ignore") as f:
            first_line = f.readline().strip()

        title = normalize_title(first_line)

        # Normalize source name (replace dashes with spaces, title case)
        source_name = source_id.replace("-", " ").title()

        metadata = {
            "source_type": "newspaper",
            "source_id": source_id,
            "source_name": source_name,
            "date": date,
            "page": page,
            "title": first_line,
            "file_path": str(path)
        }
        results.append(metadata)

        # Citation string format:
        citation = f"{source_name}, {date}, {page}, \"{title}\""
        
        print(metadata)
        print("Citation:", citation)
        print("-" * 80)
    
    return results


if __name__ == "__main__":
    process_newspapers()
