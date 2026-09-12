import json
from datetime import date

FILE_PATH = "player_details.json"


def calculate_age(dob):
    day, month, year = map(int, dob.split("-"))
    today = date.today()

    age = today.year - year

    if (today.month, today.day) < (month, day):
        age -= 1

    return str(age)


verified_players = {
    "Shubman Gill": {
        "role": "Batsman",
        "state": "Punjab",
        "date_of_birth": "08-09-1999",
        "career_status": "Active",
        "ipl_team": "Gujarat Titans",
        "achievements": "Indian international batsman and captain of the Indian Test and ODI teams. Represents Gujarat Titans in the IPL."
    },

    "Virat Kohli": {
        "role": "Batsman",
        "state": "Delhi",
        "date_of_birth": "05-11-1988",
        "career_status": "Active",
        "ipl_team": "Royal Challengers Bengaluru",
        "achievements": "Former India captain and one of India's leading international run-scorers. Winner of the 2024 T20 World Cup."
    },

    "Rohit Sharma": {
        "role": "Batsman",
        "state": "Maharashtra",
        "date_of_birth": "30-04-1987",
        "career_status": "Active",
        "ipl_team": "Mumbai Indians",
        "achievements": "Former India captain and five-time IPL champion with Mumbai Indians."
    },

    "M.S. Dhoni": {
        "role": "Wicketkeeper",
        "state": "Jharkhand",
        "date_of_birth": "07-07-1981",
        "career_status": "Retired",
        "ipl_team": "Chennai Super Kings",
        "achievements": "Led India to the 2007 T20 World Cup, 2011 ODI World Cup and 2013 Champions Trophy titles."
    },

    "Hardik Pandya": {
        "role": "All-rounder",
        "state": "Gujarat",
        "date_of_birth": "11-10-1993",
        "career_status": "Active",
        "ipl_team": "Mumbai Indians",
        "achievements": "Indian international all-rounder and former IPL captain."
    },

    "Jasprit Bumrah": {
        "role": "Bowler",
        "state": "Gujarat",
        "date_of_birth": "06-12-1993",
        "career_status": "Active",
        "ipl_team": "Mumbai Indians",
        "achievements": "One of India's leading fast bowlers across all formats."
    },

    "Ravindra Jadeja": {
        "role": "All-rounder",
        "state": "Gujarat",
        "date_of_birth": "06-12-1988",
        "career_status": "Active",
        "ipl_team": "Rajasthan Royals",
        "achievements": "Indian international all-rounder and multiple-time IPL champion."
    },

    "Rishabh Pant": {
        "role": "Wicketkeeper",
        "state": "Uttarakhand",
        "date_of_birth": "04-10-1997",
        "career_status": "Active",
        "ipl_team": "Lucknow Super Giants",
        "achievements": "Indian international wicketkeeper-batter known for match-winning performances."
    },

    "KL Rahul": {
        "role": "Wicketkeeper",
        "state": "Karnataka",
        "date_of_birth": "18-04-1992",
        "career_status": "Active",
        "ipl_team": "Delhi Capitals",
        "achievements": "Indian international wicketkeeper-batter and former IPL captain."
    },

    "Sanju Samson": {
        "role": "Wicketkeeper",
        "state": "Kerala",
        "date_of_birth": "11-11-1994",
        "career_status": "Active",
        "ipl_team": "Chennai Super Kings",
        "achievements": "Indian international wicketkeeper-batter and IPL captain."
    },

    "Suryakumar Yadav": {
        "role": "Batsman",
        "state": "Maharashtra",
        "date_of_birth": "14-09-1990",
        "career_status": "Active",
        "ipl_team": "Mumbai Indians",
        "achievements": "India T20I captain and one of the world's leading T20 batsmen."
    },

    "Ishan Kishan": {
        "role": "Wicketkeeper",
        "state": "Bihar",
        "date_of_birth": "18-07-1998",
        "career_status": "Active",
        "ipl_team": "Sunrisers Hyderabad",
        "achievements": "Indian wicketkeeper-batter and former Mumbai Indians opener."
    },

    "Shivam Dube": {
        "role": "All-rounder",
        "state": "Maharashtra",
        "date_of_birth": "26-06-1993",
        "career_status": "Active",
        "ipl_team": "Chennai Super Kings",
        "achievements": "Indian international batting all-rounder."
    },

    "Kuldeep Yadav": {
        "role": "Bowler",
        "state": "Uttar Pradesh",
        "date_of_birth": "14-12-1994",
        "career_status": "Active",
        "ipl_team": "Lucknow Super Giants",
        "achievements": "Indian left-arm wrist spinner and member of India's major ICC tournament-winning squads."
    },

    "Yuzvendra Chahal": {
        "role": "Bowler",
        "state": "Haryana",
        "date_of_birth": "23-07-1990",
        "career_status": "Active",
        "ipl_team": "Punjab Kings",
        "achievements": "India's leading T20I wicket-taking spinners."
    },

    "Ravichandran Ashwin": {
        "role": "All-rounder",
        "state": "Tamil Nadu",
        "date_of_birth": "17-09-1986",
        "career_status": "Retired",
        "ipl_team": "Chennai Super Kings",
        "achievements": "One of India's most successful Test spinners and a major international wicket-taker."
    },

    "Bhuvneshwar Kumar": {
        "role": "Bowler",
        "state": "Uttar Pradesh",
        "date_of_birth": "05-02-1990",
        "career_status": "Active",
        "ipl_team": "Royal Challengers Bengaluru",
        "achievements": "Indian swing bowler known for effective powerplay and death bowling."
    },

    "Mohammed Siraj": {
        "role": "Bowler",
        "state": "Telangana",
        "date_of_birth": "13-03-1994",
        "career_status": "Active",
        "ipl_team": "Gujarat Titans",
        "achievements": "Indian international fast bowler."
    },

    "Shreyas Iyer": {
        "role": "Batsman",
        "state": "Maharashtra",
        "date_of_birth": "06-12-1994",
        "career_status": "Active",
        "ipl_team": "Punjab Kings",
        "achievements": "Indian international batsman and IPL captain."
    },

    "Ruturaj Gaikwad": {
        "role": "Batsman",
        "state": "Maharashtra",
        "date_of_birth": "31-01-1997",
        "career_status": "Active",
        "ipl_team": "Chennai Super Kings",
        "achievements": "Indian international opening batsman and former CSK captain."
    }
}


with open(FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

updated = 0

for player_name, details in verified_players.items():
    if player_name in data:
        details["age"] = calculate_age(details["date_of_birth"])
        data[player_name].update(details)
        updated += 1
        print(f"Updated: {player_name}")
    else:
        print(f"Not found in dataset: {player_name}")


with open(FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)


print("\n====================================")
print("VERIFIED PLAYER DETAILS UPDATED")
print("====================================")
print(f"Players updated: {updated}")
print(f"Total profiles: {len(data)}")