from foundry_local_sdk import FoundryLocalManager, Configuration
import sqlite3
import json
import math
import time

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

print("Loading models...")

embedding_model = catalog.get_model("qwen3-embedding-0.6b")
embedding_model.load()
embedding_client = embedding_model.get_embedding_client()

chat_model = catalog.get_model("qwen3-0.6b")
chat_model.load()
chat_client = chat_model.get_chat_client()

print("Models loaded!\n")

def get_embedding(text):
    response = embedding_client.generate_embedding(text)
    return response.data[0].embedding

def cosine_similarity(vector1, vector2):
    dot_product = sum(a * b for a, b in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(a * a for a in vector1))
    magnitude2 = math.sqrt(sum(b * b for b in vector2))
    return dot_product / (magnitude1 * magnitude2)

def get_top_chunks(query, top_k=2):
    query_embedding = get_embedding(query)
    
    conn = sqlite3.connect("knowledge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT source, content, embedding FROM chunks")
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for source, content, embedding_json in rows:
        chunk_embedding = json.loads(embedding_json)
        score = cosine_similarity(query_embedding, chunk_embedding)
        results.append({
            "source": source,
            "content": content,
            "score": score
        })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def answer_query(question):
    top_chunks = get_top_chunks(question)
    context = "\n\n".join([chunk["content"] for chunk in top_chunks])
    
    system_message = f"""You are a strict assistant that ONLY answers using the provided context below. 
You must NEVER use any outside knowledge, even if you know the answer.
If the context does not contain the answer, respond EXACTLY with: "I don't have that information."

Context:
{context}"""
    
    response = chat_client.complete_chat(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
    )
    
    answer = response.choices[0].message.content
    if "</think>" in answer:
        answer = answer.split("</think>")[-1].strip()
    
    return answer, top_chunks

# Test cases
test_cases = [
    {"question": "What is fly-by-wire?", "should_know": True},
    {"question": "How does GPS work in aircraft?", "should_know": True},
    {"question": "What is the APU?", "should_know": True},
    {"question": "What is the price of a Boeing 747?", "should_know": False},
    {"question": "Who invented the airplane?", "should_know": False},
]

print("=" * 60)
print("RUNNING TEST SUITE")
print("=" * 60)
print()

for i, test in enumerate(test_cases, 1):
    print(f"Test {i}: {test['question']}")
    if test['should_know']:
        expected_text = "Should answer"
    else:
        expected_text = "Should say I don't know"
    print(f"Expected: {expected_text}")
    
    start_time = time.time()
    answer, sources = answer_query(test["question"])
    elapsed = time.time() - start_time
    
    print(f"Answer: {answer}")
    print(f"Time: {elapsed:.2f} seconds")
    print("-" * 60)
    print()