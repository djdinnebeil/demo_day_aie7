from qdrant_client.models import Filter, FieldCondition, MatchValue
from db import ensure_db, delete_document, file_sha256

def delete_document_from_store(con, client, collection_name: str, doc_id: str) -> None:
    """Delete a document from SQLite and Qdrant using its doc_id."""

    # 1. Delete from Qdrant
    client.delete(
        collection_name=collection_name,
        wait=True,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="metadata.doc_id",  # always nested
                    match=MatchValue(value=str(doc_id))
                )
            ]
        ),
    )

    # 2. Delete from SQLite
    delete_document(con, doc_id)
    print(f"Deleted document {doc_id} from DB and Qdrant.")
