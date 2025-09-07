import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import json

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

embedding_model = OpenAIEmbeddings( api_key=OPENAI_API_KEY, model="text-embedding-3-small")

def initialize_faiss_vectorstore(chunks):
    return FAISS.from_texts(chunks, embedding=embedding_model)

boc_chunks_path = "./Docs/boc_chunks.jsonl"
chunks = []
with open(boc_chunks_path, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        if "content" in obj and obj["content"].strip():
            chunks.append(obj["content"].strip())
        elif "question" in obj and "answer" in obj:
            text = f"Q: {obj['question'].strip()}\nA: {obj['answer'].strip()}"
            chunks.append(text)

vectorstore = initialize_faiss_vectorstore(chunks)

print(f"Loaded {len(chunks)} chunks from boc_chunks.jsonl")