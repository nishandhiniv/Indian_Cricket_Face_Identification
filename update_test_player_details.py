import json
from datetime import date

FILE_PATH = "player_details.json"


def calculate_age(date_of_birth):
    day, month, year = map(int, date_of_birth.split("-"))
    today = date.today()

    age = today.year - year

    if (today.month, today.day) < (month, day):
        age -= 1

    return str(age)


test_details = {
    "M.S. Dhoni": {
        "role": "Wicketkeeper",
        "state": "Jharkhand",
        "date_of_birth": "07-07-1981",
        "career_status": "Retired",
        "ipl_team": "Chennai Super Kings",
        "achievements": "Former India captain; led India to the 2007 T20 World Cup and 2011 ODI World Cup titles."
    },
    "Virat Kohli": {
        "role": "Batsman",
        "state": "Delhi",
        "date_of_birth": "05-11-1988",
        "career_status": "Active",
        "ipl_team": "Royal Challengers Bengaluru",
        "achievements": "Former India captain and one of India's leading international run-scorers."
    },
    "Rohit Sharma": {
        "role": "Batsman",
        "state": "Maharashtra",
        "date_of_birth": "30-04-1987",
        "career_status": "Active",
        "ipl_team": "Mumbai Indians",
        "achievements": "Led India to the 2024 T20 World Cup title; five-time IPL champion as Mumbai Indians captain."
    },
    "Hardik Pandya": {
        "role": "All-rounder",
        "state": "Gujarat",
        "date_of_birth": "11-10-1993",
        "career_status": "Active",
        "ipl_team": "Mumbai Indians",
        "achievements": "India international all-rounder and former Mumbai Indians captain."
    },
    "Sachin Tendulkar": {
        "role": "Batsman",
        "state": "Maharashtra",
        "date_of_birth": "24-04-1973",
        "career_status": "Retired",
        "ipl_team": "Mumbai Indians",
        "achievements": "First male cricketer to score a double century in ODI cricket; 100 international centuries."
    }
}


with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

for player_name, details in test_details.items():
    if player_name in data:
        details["age"] = calculate_age(details["date_of_birth"])

        data[player_name].update(details)
        print(f"Updated: {player_name}")
    else:
        print(f"Player not found: {player_name}")

with open(FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("\nTEST PLAYER DETAILS UPDATED SUCCESSFULLY")
print(f"Total player profiles: {len(data)}")