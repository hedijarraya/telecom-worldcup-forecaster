import pandas as pd
import random
from datetime import datetime, timedelta
import os

# -----------------------------
# 1. BASE DATA
# -----------------------------
teams = [
    "France", "Brazil", "Germany", "Argentina",
    "Spain", "England", "Portugal", "Morocco",
    "USA", "Italy", "Netherlands", "Belgium",
    "Tunisia"
]

cities = {
    "New York":    {"tz": "America/New_York",    "utc_offset": -4},
    "Los Angeles": {"tz": "America/Los_Angeles", "utc_offset": -7},
    "Dallas":      {"tz": "America/Chicago",     "utc_offset": -5},
    "Miami":       {"tz": "America/New_York",    "utc_offset": -4},
    "Mexico City": {"tz": "America/Mexico_City", "utc_offset": -5},
    "Toronto":     {"tz": "America/Toronto",     "utc_offset": -4},
}

stades = {
    "New York":    "MetLife Stadium",
    "Los Angeles": "SoFi Stadium",
    "Dallas":      "AT&T Stadium",
    "Miami":       "Hard Rock Stadium",
    "Mexico City": "Estadio Azteca",
    "Toronto":     "BMO Field",
}

phases = ["Group Stage", "Round of 16", "Quarter Final", "Semi Final", "Final"]

phase_importance = {
    "Group Stage":   1,
    "Round of 16":   2,
    "Quarter Final": 3,
    "Semi Final":    4,
    "Final":         5
}

# -----------------------------
# 2. MATCH GENERATION
# -----------------------------
num_matches = 40
start_date = datetime(2026, 6, 11)
data = []
used_pairs = set()

for i in range(num_matches):
    attempts = 0
    while True:
        team_a, team_b = random.sample(teams, 2)
        pair = tuple(sorted([team_a, team_b]))
        if pair not in used_pairs or attempts > 50:
            used_pairs.add(pair)
            break
        attempts += 1

    city = random.choice(list(cities.keys()))
    city_info = cities[city]
    utc_offset = city_info["utc_offset"]

    phase = random.choices(
        phases,
        weights=[0.5, 0.2, 0.15, 0.1, 0.05]
    )[0]
    importance = phase_importance[phase]

    match_date = start_date + timedelta(days=random.randint(0, 35))
    local_hour = random.choice([14, 17, 20])
    utc_hour = (local_hour - utc_offset) % 24

    match = {
        "match_id":       i + 1,
        "date":           match_date.date().isoformat(),
        "heure_locale":   f"{local_hour:02d}:00",
        "fuseau_horaire": city_info["tz"],
        "heure_utc":      f"{utc_hour:02d}:00",
        "pays_a":         team_a,
        "pays_b":         team_b,
        "ville":          city,
        "stade":          stades[city],
        "phase":          phase,
        "importance":     importance
    }
    data.append(match)

df = pd.DataFrame(data)
df = df.sort_values(["date", "heure_utc"]).reset_index(drop=True)
df["match_id"] = df.index + 1

# -----------------------------
# 3. EXPORT CSV
# -----------------------------
os.makedirs("data", exist_ok=True)
df.to_csv("data/matches.csv", index=False, encoding="utf-8")
print(f"✅ Dataset créé : {df.shape[0]} matchs, {df.shape[1]} colonnes")
print(df.head(10).to_string())