import requests
import pandas as pd
from tqdm import tqdm

base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/"
comp_url = base_url + "matches/[]/[].json"
match_url = base_url + "events/{}.json"


