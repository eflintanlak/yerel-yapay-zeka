from foundry_local_sdk import FoundryLocalManager, Configuration
import os
import sqlite3
import json

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-embedding-0.6b")
model.load()
client = model.get_embedding_client()

documents_folder = "documents"

def load_and_chunk_documents():
    all_chunks = []
    files = os.listdir(documents_folder)
    
    for filename in files:
        filepath = os.path.join(documents_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        paragraphs = content.split("\n\n")
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if len(paragraph) < 40:
                continue
            all_chunks.append({
                "source": filename,
                "text": paragraph
            })
    
    return all_chunks

def get_embedding(text):
    response = client.generate_embedding(text)
    return response.data[0].embedding

# Set up database
conn = sqlite3.connect("knowledge.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY,
        source TEXT,
        content TEXT,
        embedding TEXT
    )
""")

# Clear old data to avoid duplicates when re-running
cursor.execute("DELETE FROM chunks")

# Load, embed, and save each chunk
chunks = load_and_chunk_documents()
print(f"Processing {len(chunks)} chunks...\n")

for chunk in chunks:
    embedding = get_embedding(chunk["text"])
    embedding_json = json.dumps(embedding)
    
    cursor.execute(
        "INSERT INTO chunks (source, content, embedding) VALUES (?, ?, ?)",
        (chunk["source"], chunk["text"], embedding_json)
    )
    print(f"Saved: {chunk['source']} -> {chunk['text'][:50]}...")

conn.commit()
conn.close()

print(f"\nAll {len(chunks)} chunks saved to database!")