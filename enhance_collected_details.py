import json
import re

FILE_PATH = "player_details.json"

with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

updated = 0

for player_name, details in data.items():

    if details.get("source") != "Wikipedia":
        continue

    biography = details.get("biography", "")
    text = biography.lower()

    # Role improvement
    if "wicket-keeper" in text or "wicketkeeper" in text:
        details["role"] = "Wicketkeeper"
    elif "all-rounder" in text or "allrounder" in text:
        details["role"] = "All-rounder"
    elif "bowler" in text:
        details["role"] = "Bowler"
    elif "batsman" in text or "batter" in text:
        details["role"] = "Batsman"

    # Career status
    if "retired from all forms" in text or "former indian cricketer" in text:
        details["career_status"] = "Retired"
    elif "former cricketer" in text and "current" not in text:
        details["career_status"] = "Retired"
    elif "indian cricketer" in text:
        details["career_status"] = "Active / To be verified"

    # IPL team extraction
    ipl_teams = [
        "Chennai Super Kings",
        "Mumbai Indians",
        "Royal Challengers Bengaluru",
        "Royal Challengers Bangalore",
        "Gujarat Titans",
        "Lucknow Super Giants",
        "Delhi Capitals",
        "Delhi Daredevils",
        "Kolkata Knight Riders",
        "Rajasthan Royals",
        "Punjab Kings",
        "Kings XI Punjab",
        "Sunrisers Hyderabad",
        "Deccan Chargers"
    ]

    found_teams = []

    for team in ipl_teams:
        if team.lower() in text:
            found_teams.append(team)

    if found_teams:
        details["ipl_team"] = found_teams[-1]

    # Use biography as achievements when actual achievement field is unavailable
    if details.get("achievements") in [
        "Player profile details are being verified.",
        "Not Available"
    ]:
        details["achievements"] = details.get(
            "biography",
            "Player achievements are being verified."
        )

    updated += 1

with open(FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("COLLECTED PLAYER DETAILS ENHANCED")
print(f"Profiles enhanced: {updated}")
print(f"Total profiles: {len(data)}")