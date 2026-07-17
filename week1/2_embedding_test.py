from foundry_local_sdk import FoundryLocalManager, Configuration

config = Configuration(app_name="local-ai-assistant")
manager = FoundryLocalManager(config)
catalog = manager.catalog

model = catalog.get_model("qwen3-embedding-0.6b")

print("Downloading model...")
model.download()
print(f"Cached: {model.is_cached}")

model.load()
client = model.get_embedding_client()

sentences = [
    "The cat is sleeping",
    "The cat took a nap",
    "The car is going fast"
]

for sentence in sentences:
    response = client.generate_embedding(sentence)
    embedding = response.data[0].embedding
    print(f"'{sentence}'")
    print(f"  First 3 values: {embedding[:3]}")
    print()