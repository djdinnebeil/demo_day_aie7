from langchain.text_splitter import RecursiveCharacterTextSplitter

def adaptive_chunk_documents(text: str, model: str = 'text-embedding-3-small'):
    # Count tokens
    import tiktoken
    enc = tiktoken.encoding_for_model(model)
    token_count = len(enc.encode(text))

    if token_count < 500:
        # Keep whole document
        return [text]
    elif token_count < 1500:
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=model, chunk_size=500, chunk_overlap=80
        )
    else:
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=model, chunk_size=800, chunk_overlap=100
        )

    return splitter.create_documents([text])