from qdrant_client import QdrantClient

# --- Settings ---
COLLECTION_NAME = "amatol_docs"   # change if needed
HOST = "localhost"
PORT = 6333

def delete_collection(name: str):
    client = QdrantClient(host=HOST, port=PORT)

    if client.collection_exists(name):
        client.delete_collection(name)
        print(f"Collection '{name}' deleted successfully.")
    else:
        print(f"Collection '{name}' does not exist.")

import os
from pathlib import Path

DB_PATH = Path("data/amatol_index.sqlite")

def delete_sqlite_db():
    if DB_PATH.exists():
        os.remove(DB_PATH)
        print(f"Deleted database file: {DB_PATH}")
    else:
        print(f"No database found at: {DB_PATH}")

if __name__ == "__main__":
    delete_collection(COLLECTION_NAME)
    delete_sqlite_db()
