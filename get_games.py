import requests
import json
import time

# RAWG API base URL
BASE_URL = "https://api.rawg.io/api/games"
API_KEY = "f098286ad1a045f1a00a3023aea4de01" 
games = []
page = 1

while page <= 5:
    url = f"{BASE_URL}?key={API_KEY}&page={page}&page_size=100"
    response = requests.get(url)
    if response.status_code != 200:
        print("Request failed:", response.status_code)
        break

    data = response.json()
    for game in data["results"]:
        games.append({
            "name": game["name"],
            "description": game.get("description_raw", ""),  # may be empty
            "platforms": [p["platform"]["name"] for p in game.get("platforms", [])]
        })

    print(f"Page {page} done, total games collected: {len(games)}")
    page += 1
    time.sleep(1)

# Save to JSON
with open("rawg_games.json", "w", encoding="utf-8") as f:
    json.dump(games, f, indent=2)

print("Saved", len(games), "games to games_list.json")