import sqlite3, hashlib, uuid
from pathlib import Path
from datetime import datetime

DB_PATH = Path('./data/amatol_index.sqlite')

def ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""
    CREATE TABLE IF NOT EXISTS documents (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    path         TEXT,
    citation     TEXT,
    source_type  TEXT,
    source_id    TEXT,
    date         TEXT,
    num_chunks   INTEGER,
    content_hash TEXT UNIQUE,
    added_at     DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    return con

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def document_exists(con, content_hash: str) -> bool:
    cur = con.execute("SELECT 1 FROM documents WHERE content_hash = ?", (content_hash,))
    return cur.fetchone() is not None

def insert_document(con, path: Path, parsed: dict, content_hash: str, num_chunks: int) -> None:
    md = parsed['metadata']
    con.execute("""
    INSERT INTO documents (path, citation, source_type, source_id, date, content_hash, num_chunks, added_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(path),
        md.get('citation'),
        md.get('source_type'),
        md.get('source_id'),
        md.get('date'),
        content_hash,
        num_chunks,
        datetime.utcnow().isoformat()
    ))

def delete_document(con, content_hash: str) -> None:
    """Delete a document row by its content hash."""
    con.execute("DELETE FROM documents WHERE content_hash = ?", (content_hash,))
    con.commit()


def list_documents(con):
    cur = con.execute("SELECT path, citation, source_id, date, num_chunks, added_at FROM documents ORDER BY added_at DESC")
    return cur.fetchall()

def list_all_documents(con):
    cur = con.execute("SELECT * FROM documents ORDER BY added_at DESC")
    return cur.fetchall()

if __name__ == "__main__":
    con = ensure_db()
    print(list_all_documents(con))