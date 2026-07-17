from foundry_local_sdk import FoundryLocalManager, Configuration
import math
config = Configuration(app_name="local-artificial-intelligence")
manager = FoundryLocalManager(config)
catalog = manager.catalog
model = catalog.get_model("qwen3-embedding-0.6b")
model.load()
client = model.get_embedding_client()
def cosine_similarity(vektor1, vektor2):
    dot_product = sum(a * b for a, b in zip(vektor1, vektor2))
    
