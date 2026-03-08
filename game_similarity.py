import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load AI embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load games JSON

with open("games_list.json", "r", encoding="utf-8") as f:
    games = json.load(f)

print("Creating embeddings for games...")

# Create embeddings for each game

for game in games:
    text = game["name"]
    if "description" in game:
        text += " " + game["description"]
    # Convert text to AI embedding
    game["embedding"] = model.encode(text)

print("Embeddings created for", len(games), "games")

# Cosine similarity function

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
while True:
    idea = input("\nEnter your game idea (or 'quit'): ")
    if idea.lower() == "quit":
        break
    # Convert idea to embedding
    idea_embedding = model.encode(idea)
    results = []
    # Compare idea with every game
    for game in games:
        similarity = cosine_similarity(idea_embedding, game["embedding"])
        results.append({
            "name": game["name"],
            "platforms": game.get("platforms", []),
            "similarity": similarity
        })
    # Sort best matches
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:10]
    print("\nTop 10 similar games:\n")
    for r in results:
        platforms = ", ".join(r["platforms"]) if r["platforms"] else "N/A"
        percent = r["similarity"] * 100
        print(f"{r['name']} ({platforms}) -> {percent:.2f}% similar")