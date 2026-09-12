import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "indian cricketer"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "player_details.json"
)

player_details = {}

if not os.path.exists(DATASET_DIR):
    raise FileNotFoundError(
        f"Dataset folder not found: {DATASET_DIR}"
    )

player_folders = sorted(
    [
        name
        for name in os.listdir(DATASET_DIR)
        if os.path.isdir(
            os.path.join(DATASET_DIR, name)
        )
    ]
)

for player_name in player_folders:
    player_details[player_name] = {
        "role": "Indian Cricketer",
        "batting_style": "Information available soon",
        "bowling_style": "Information available soon",
        "country": "India",
        "achievement": "Player profile under development",
        "about": (
            f"{player_name} is an Indian cricketer "
            "included in the face identification dataset."
        )
    }

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        player_details,
        file,
        indent=4,
        ensure_ascii=False
    )

print("=" * 60)
print("PLAYER DETAILS FILE GENERATED")
print("=" * 60)
print(f"Total player profiles: {len(player_details)}")
print(f"Saved to: {OUTPUT_FILE}")
print("=" * 60)