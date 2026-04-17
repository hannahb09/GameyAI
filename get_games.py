import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = "https://api.rawg.io/api/games"
API_KEY = os.getenv("RAWG_API_KEY")
print(API_KEY)

games = []
page = 1
TOTAL_PAGES = 5

while page <= TOTAL_PAGES:
    url = f"{BASE_URL}?key={API_KEY}&page={page}&page_size=100"
    response = requests.get(url)
    if response.status_code != 200:
        print("Request failed:", response.status_code)
        break
    data = response.json()
    for game in data["results"]:
        games.append({
            "name": game["name"],
            "slug": game["slug"],
            "description": "",
            "platforms": [p["platform"]["name"] for p in game.get("platforms", [])]
        })
        print(f"Page {page} done, total games collected: {len(games)}")
        page += 1
        time.sleep(1)
    
    for i, game in enumerate(games):
        url = f"{BASE_URL}/{game['slug']}?key={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            game["description"] = data.get("description_raw", "")
        else:
            print(f"Failed to get description for {game['name']}")
        if (i + 1) % 50 == 0:
            print(f"Fetched descriptions for {i + 1} games")
        time.sleep(0.5)

# Save to JSON
with open("rawg_games.json", "w", encoding="utf-8") as f:
    json.dump(games, f, indent=2)

print("Saved", len(games), "games to rawg_games.json")