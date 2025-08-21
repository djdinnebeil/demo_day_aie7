import os
from pathlib import Path

ROOT_DIR = "amatol/books"

def normalize_source_name(source_id: str) -> str:
    """Convert a folder name like 'amatol_book' → 'Amatol Book'."""
    return source_id.replace("_", " ").title()

def extract_book_metadata(root_dir: str = ROOT_DIR):
    results = []
    for path in Path(root_dir).rglob("*.txt"):
        # Get parts of the path
        source_type = "book"
        source_id = path.parent.name        # e.g. 'amatol_book'
        source_name = normalize_source_name(source_id)
        page = path.stem                    # filename without .txt (e.g. 'p007')
        file_path = str(path)

        metadata = {
            "source_type": source_type,
            "source_id": source_id,
            "source_name": source_name,
            "page": page,
            "file_path": file_path,
        }
        results.append(metadata)
    return results

if __name__ == "__main__":
    metadata_list = extract_book_metadata()
    for m in metadata_list:
        print(m)
