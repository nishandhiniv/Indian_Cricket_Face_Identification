import json
import os

FILE_PATH = "player_details.json"

rename_map = {
    "Anil Kumble1": "Anil Kumble",
    "Ashish Nehra1": "Ashish Nehra",
    "Harbhajan Singh1": "Harbhajan Singh",
    "M.S. Dhoni1": "M.S. Dhoni",
    "Rahul Dravid2": "Rahul Dravid",
    "Sourav Ganguly1": "Sourav Ganguly",
    "Virender Sehwag2": "Virender Sehwag",
    "Yuvraj Singh1": "Yuvraj Singh",
    "Zaheer Khan1": "Zaheer Khan"
}

if not os.path.exists(FILE_PATH):
    print("ERROR: player_details.json not found")
    exit()

with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

updated_data = {}

for player_name, details in data.items():
    new_name = rename_map.get(player_name, player_name)
    updated_data[new_name] = details

with open(FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(updated_data, file, indent=4, ensure_ascii=False)

print("PLAYER NAMES CLEANED SUCCESSFULLY")
print("Updated names:")

for old_name, new_name in rename_map.items():
    print(f"{old_name} -> {new_name}")

print(f"\nTotal player profiles: {len(updated_data)}")