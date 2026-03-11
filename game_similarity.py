import json
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Load games JSON

with open("rawg_games.json", "r", encoding="utf-8") as f:
    games = json.load(f)
print("Processing game descriptions...")

# Create embeddings for each game

for game in games:
    text = game["name"]
    if game.get("description"):
        text += " " + game["description"]
    game["doc"] = nlp(text)

print(f"Processed {len(games)} games")

while True:
    idea = input("\nEnter your game idea (or 'quit'): ")
    if idea.lower() == "quit":
        break
    idea_doc = nlp(idea)
    results = []
    # Compare idea with every game
    for game in games:
        similarity = idea_doc.similarity(game["doc"])
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