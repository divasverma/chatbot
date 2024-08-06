import faiss
import os
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.faiss import FaissVectorStore

# dimensions of text-ada-embedding-002
d = 1536
faiss_index = faiss.IndexFlatL2(d)
my_directory_path = "/Users/divasverma/Desktop/ai-playground/llamaindex-tutorials/2-GUI_travel_recommendation_RAG/documents"

documents = SimpleDirectoryReader(my_directory_path).load_data()

# Create a VectorStoreIndex from the loaded documents

vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
index.storage_context.persist()
