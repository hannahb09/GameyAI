import requests
import json
import time

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
with open("rawg_games.json", "r", encoding="utf-8") as f:
    games = json.load(f)