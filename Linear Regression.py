# required imports
import requests
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

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

        passes = [x for x in events if x['type']['name'] == "Pass"]

        for a in passes:
            attributes = {
                "player_id": a['player']['id'],
                "outcome": 0 if 'outcome' in a['pass'].keys() else 1,
            }
            all_events.append(attributes)

    return pd.DataFrame(all_events)


comp_id = 43
seas_id = 3

df = parse_data(comp_id, seas_id)

print(df.head(15))

total_passes = df.groupby('player_id')['outcome'].sum()
percentage = df.groupby('player_id')['outcome'].mean()

model = LinearRegression()
fit = model.fit([[x] for x in total_passes], percentage)
print("Coefficients: {}:".format(fit.coef_))
print("Intercept: {}:".format(fit.intercept_))

xfit = [0,500]
yfit = model.predict([[x] for x in xfit])

plt.scatter(total_passes, percentage, alpha=0.8)
plt.plot(xfit,yfit, 'r')
plt.show()