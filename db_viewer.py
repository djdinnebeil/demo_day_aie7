import streamlit as st
from pathlib import Path
from db import ensure_db, list_documents, delete_document
from vector_delete import delete_document_from_store
from qdrant_client import QdrantClient

st.set_page_config(page_title="Historical Research Assistant", layout="wide")
st.title("📜 Historical Research Assistant – File Manager")

# Ensure DB connection
con = ensure_db()
client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "amatol_docs"

# Fetch documents
docs = list_documents(con)

if not docs:
    st.info("No documents uploaded yet.")
else:
    for path, citation, source_id, date, num_chunks, added_at in docs:
        with st.container():
            col1, col2, col3 = st.columns([4, 1, 1])
            
            # File info
            with col1:
                st.write(f"**{Path(path).name}**")
                st.caption(f"Citation: {citation or '—'} | Chunks: {num_chunks} | Added: {added_at}")

            # View button
            with col2:
                if st.button("View", key=f"view-{path}"):
                    with open(path, "r", encoding="utf-8") as f:
                        file_content = f.read()

                    @st.dialog(f"Contents of {Path(path).name}")
                    def show_file():
                        st.text_area("File Content", file_content, height=400)

                    show_file()

            # Delete button
            with col3:
                if st.button("Delete", key=f"delete-{path}"):
                    from db import file_sha256
                    content_hash = file_sha256(Path(path))
                    delete_document_from_store(con, client, COLLECTION_NAME, content_hash)
                    st.success(f"Deleted {Path(path).name}")
                    st.rerun()
