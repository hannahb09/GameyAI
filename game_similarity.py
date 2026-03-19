import json
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# Function to clean text
def preprocess(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(tokens)

# Load games JSON

with open("rawg_games.json", "r", encoding="utf-8") as f:
    games = json.load(f)
print("Processing game descriptions...")

# Create embeddings for each game

for game in games:
    description = game.get("description", "")
    text = (description * 2) + " " + game["name"]
    clean_text = preprocess(text)
    game["doc"] = nlp(clean_text)

print(f"Processed {len(games)} games")

while True:
    idea = input("\nEnter your game idea (or 'quit'): ")
    if idea.lower() == "quit":
        break
    idea_clean = preprocess(idea)
    idea_doc = nlp(idea_clean)
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