# required imports
import requests
import pandas as pd
from tqdm import tqdm

# setting the urls for later use
base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/"
comp_url = base_url + "matches/{}/{}.json"
match_url = base_url + "events/{}.json"

# function to parse data into pandas DataFrame


def parse_data(competition_id, season_id):
    matches = requests.get(url=comp_url.format(competition_id, season_id)).json()
    match_ids = [m['match_id'] for m in matches]

    all_events = []

    for match_id in tqdm(match_ids):

        events = requests.get(url=match_url.format(match_id)).json()

        shots = [x for x in events if x['type']['name'] == "Shot"]

        for s in shots:
            attributes = {
                "match_id": match_id,
                "team": s["possession_team"]["name"],
                "player": s['player']['name'],
                "x": s['location'][0],
                "y": s['location'][1],
                "outcome": s['shot']['outcome']['name'],
            }
            all_events.append(attributes)

    return pd.DataFrame(all_events)


comp_id = 43
seas_id = 3

df = parse_data(43, 3)

print(df.head(10))