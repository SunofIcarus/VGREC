import json
from pathlib import Path

CACHE_FILE = Path("data/embeddings_cache.json")

def load_embedding_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_embedding_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def get_cached_embedding(text: str, cache: dict) -> str:
    return cache.get(text.strip().lower())

def update_embedding_cache(text: str, embedding: list, cache: dict):
    cache[text.strip().lower()] = embedding
    save_embedding_cache(cache)

if __name__ == "__main__":
    test_cache = load_embedding_cache()
    update_embedding_cache("test_text", [0.1, 0.2, 0.3], test_cache)
    print(get_cached_embedding("test_text", test_cache))