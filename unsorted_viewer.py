import streamlit as st
from pathlib import Path
import tempfile

from unsorted_db import ensure_db, file_sha256, insert_document, delete_document, list_documents, document_exists
from unsorted_parser import parse_unsorted

st.set_page_config(page_title="Unsorted Documents", layout="wide")
st.title("📂 Unsorted Historical Documents")

# DB connection
con = ensure_db()

# --- Upload Section ---
st.header("Upload a Document")
uploaded = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded is not None:
    # Save to temp file
    tmp_dir = Path(tempfile.mkdtemp())
    tmp_path = tmp_dir / uploaded.name
    tmp_path.write_bytes(uploaded.getbuffer())

    # Parse + hash
    parsed = parse_unsorted(str(tmp_path))
    h = file_sha256(tmp_path)

    if document_exists(con, h):
        st.warning("This document already exists in the database.")
    else:
        insert_document(con, tmp_path, parsed, h, num_chunks=1)
        con.commit()
        st.success(f"Uploaded: {uploaded.name}")
        st.rerun()

# --- Document List ---
st.header("Stored Documents")
docs = list_documents(con)

if not docs:
    st.info("No documents stored yet.")
else:
    for path, citation, source_id, date, num_chunks, added_at in docs:
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.write(f"**{Path(path).name}**")
                st.caption(f"Citation: {citation or '—'} | Date: {date or '—'} | Added: {added_at}")

            with col2:
                if st.button("View", key=f"view-{path}"):
                    with open(path, "r", encoding="utf-8") as f:
                        file_content = f.read()

                    @st.dialog(f"Contents of {Path(path).name}")
                    def show_file():
                        st.text_area("File Content", file_content, height=400)

                    show_file()

            with col3:
                if st.button("Delete", key=f"delete-{path}"):
                    h = file_sha256(Path(path))
                    delete_document(con, h)
                    st.success(f"Deleted {Path(path).name}")
                    st.rerun()
