import os
import json

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

JSON_FILE = os.path.join(
    BASE_DIR,
    "player_details.json"
)

if not os.path.exists(JSON_FILE):
    raise FileNotFoundError(
        "player_details.json not found"
    )

with open(
    JSON_FILE,
    "r",
    encoding="utf-8"
) as file:
    old_details = json.load(file)


new_details = {}

for player_name in old_details:

    new_details[player_name] = {
        "role": "Information available soon",
        "state": "Information available soon",
        "date_of_birth": "Information available soon",
        "age": "Information available soon",
        "career_status": "Information available soon",
        "ipl_team": "Information available soon",
        "achievements": "Information available soon"
    }


with open(
    JSON_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        new_details,
        file,
        indent=4,
        ensure_ascii=False
    )


print("=" * 60)
print("PLAYER DETAILS FORMAT UPDATED")
print("=" * 60)
print(f"Total player profiles: {len(new_details)}")
print("Removed: About Player")
print("Added: Role, State, DOB, Age, Career Status, IPL Team, Achievements")
print("=" * 60)