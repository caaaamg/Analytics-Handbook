# required imports
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/"
comp_url = base_url + "matches/{}/{}.json"
match_url = base_url + "events/{}.json"


def parse_data(competition_id, season_id):
    matches = requests.get(url=comp_url.format(competition_id, season_id)).json()
    match_ids = [m['match_id'] for m in matches]

    all_events = []

    for match_id in tqdm(match_ids):

        events = requests.get(url=match_url.format(match_id)).json()
        shots = [x for x in events if x['type']['name'] == "Shot"]

        for s in shots:
            attributes = {
                "x": s['location'][0],
                "y": s['location'][0],
                "head": 1 if s['shot']['body_part']['name'] == "Head" else 0,
                "phase": s['shot']['type']['name'],
                "outcome": 1 if s['shot']['outcome']['name'] == "Goal" else 0,
                "statsbomb_xg": s['shot']['statsbomb_xg']
            }
            all_events.append(attributes)

    return pd.DataFrame(all_events)


comp_id = 43
seas_id = 3
df = parse_data(comp_id, seas_id)

# Determines distance to goal based on shot x and y


def distance_to_goal(origin):
    dest = np.array([120., 40.])
    return np.sqrt(np.sum((origin-dest) ** 2))

# angle of the goal that is open to the shooter


def goal_angle(origin):
    p0 = np.array((120., 36.))  # left post
    p1 = np.array(origin, dtype=np.float)
    p2 = np.array((120., 44.))  # right post

    v0 = p0 - p1
    v1 = p2 - p1

    angle = np.abs(np.math.atan2(np.linalg.det([v0, v1]), np.dat(v0, v1)))

    return angle


