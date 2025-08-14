import os
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from src.helper import load_pdf_files, process_documents
import json

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX")

embedding_model = OpenAIEmbeddings( api_key=OPENAI_API_KEY, model="text-embedding-3-small", disallowed_special=())

# boc_chunks_path = "./Docs/boc_chunks.jsonl"
# chunks = []
# with open(boc_chunks_path, "r", encoding="utf-8") as f:
#     for line in f:
#         obj = json.loads(line)
#         if "content" in obj and obj["content"].strip():
#             chunks.append(obj["content"].strip())
#         elif "question" in obj and "answer" in obj:
#             text = f"Q: {obj['question'].strip()}\nA: {obj['answer'].strip()}"
#             chunks.append(text)

# print(f"Loaded {len(chunks)} chunks from boc_chunks.jsonl")


pdf_folder_path = "Docs/"
extracted_documents = load_pdf_files(pdf_folder_path)
splits = process_documents(extracted_documents)

PineconeVectorStore.from_texts([t.page_content for t in splits], embedding=embedding_model,index_name=PINECONE_INDEX, namespace="boc" )

# PineconeVectorStore.from_texts(
#     texts=chunks,
#     embedding=embedding_model,
#     index_name=PINECONE_INDEX,
#     namespace="boc"
# )