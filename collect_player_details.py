import json
import urllib.parse
import urllib.request
import re
import time

FILE_PATH = "player_details.json"


def wikipedia_summary(player_name):
    try:
        search_url = (
            "https://en.wikipedia.org/w/api.php?"
            + urllib.parse.urlencode({
                "action": "query",
                "list": "search",
                "srsearch": player_name + " Indian cricketer",
                "format": "json",
                "srlimit": 1
            })
        )

        request = urllib.request.Request(
            search_url,
            headers={"User-Agent": "CricketFaceIdentificationProject/1.0"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))

        search_results = result.get("query", {}).get("search", [])

        if not search_results:
            return None

        title = search_results[0]["title"]

        summary_url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + urllib.parse.quote(title.replace(" ", "_"))
        )

        request = urllib.request.Request(
            summary_url,
            headers={"User-Agent": "CricketFaceIdentificationProject/1.0"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            summary = json.loads(response.read().decode("utf-8"))

        return summary

    except Exception:
        return None


with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

total = len(data)
processed = 0
found = 0

for player_name, details in data.items():
    processed += 1

    # Skip profiles already containing real details
    if details.get("role") not in ["Not Available", "Information available soon"]:
        print(f"[{processed}/{total}] Preserved: {player_name}")
        continue

    print(f"[{processed}/{total}] Searching: {player_name}")

    summary = wikipedia_summary(player_name)

    if summary:
        description = summary.get("description", "")
        extract = summary.get("extract", "")

        details["source"] = "Wikipedia"
        details["wikipedia_title"] = summary.get("title", player_name)

        if description:
            details["profile_description"] = description

        if extract:
            details["biography"] = extract[:1000]

        # Basic role detection from verified summary text
        text = (description + " " + extract).lower()

        if "wicket-keeper" in text or "wicketkeeper" in text:
            details["role"] = "Wicketkeeper"
        elif "all-rounder" in text or "allrounder" in text:
            details["role"] = "All-rounder"
        elif "bowler" in text:
            details["role"] = "Bowler"
        elif "batsman" in text or "batter" in text:
            details["role"] = "Batsman"

        found += 1
    else:
        details["source"] = "Not found"

    time.sleep(0.3)

with open(FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("\n====================================")
print("PLAYER DATA COLLECTION COMPLETED")
print("====================================")
print(f"Total profiles: {total}")
print(f"Profiles with online data: {found}")
print("Saved file: player_details.json")