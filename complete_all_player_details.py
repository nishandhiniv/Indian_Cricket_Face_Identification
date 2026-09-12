import json
from datetime import date

FILE_PATH = "player_details.json"

with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

default_details = {
    "role": "Not Available",
    "state": "Not Available",
    "date_of_birth": "Not Available",
    "age": "Not Available",
    "career_status": "To be verified",
    "ipl_team": "Not Available / No confirmed IPL team",
    "achievements": "Player profile details are being verified."
}

updated_count = 0
preserved_count = 0

for player_name, details in data.items():

    # Preserve already completed real details
    if details.get("role") != "Information available soon":
        preserved_count += 1
        continue

    # Fill missing profile fields safely
    for key, value in default_details.items():
        if not details.get(key) or details.get(key) == "Information available soon":
            details[key] = value

    updated_count += 1

with open(FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("ALL PLAYER DETAILS STRUCTURE COMPLETED")
print(f"Newly completed profiles: {updated_count}")
print(f"Existing real profiles preserved: {preserved_count}")
print(f"Total player profiles: {len(data)}")