from helper import initialize_model, initialize_database_and_memory

def initialize_app():
    embedding_function, llm, chroma_client = initialize_model()
    message_history, memory, chunk_store = initialize_database_and_memory()
    return embedding_function, llm, chroma_client, message_history, memory, chunk_store
