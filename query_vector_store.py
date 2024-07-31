import os
from llama_index.core import (
    load_index_from_storage,
    StorageContext,
)
os.environ["OPENAI_API_KEY"] = "sk-None-vswA6kIBQohsQcsRC3NVT3BlbkFJ2sqPSdAyLw42KLzWomCn"
from llama_index.vector_stores.faiss import FaissVectorStore

def query_vector_index(prompt):

    # load index from disk
    vector_store = FaissVectorStore.from_persist_dir("./storage")
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store, persist_dir="./storage"
    )
    index = load_index_from_storage(storage_context=storage_context)


    # set Logging to DEBUG for more detailed outputs
    query_engine = index.as_query_engine()
    response = query_engine.query(prompt)
    return response
