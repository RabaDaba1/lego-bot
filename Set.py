from Scraper import SetScraper
import pandas as pd

sets_csv = './database/sets.csv'

def add_set(set_id: int):
    # Append set to sets.csv
    df = pd.read_csv(sets_csv)

    if set_id in df['set_id']:
        print(f'Set {set_id} is already in database')
        return
    
    df = pd.concat([df, pd.DataFrame([{ 'set_id': 40539 }])], ignore_index=True)
    df.to_csv(sets_csv, index=False)

def delete_set(set_id: int):
    # Delete set from sets.csv
    df = pd.read_csv(sets_csv)

    if set_id not in df['set_id']:
        print(f'Set {set_id} is not in database')
        return

    df = df[df['set_id'] != set_id]
    df.to_csv(sets_csv, index=False)

class Set:
    set_id: int
    offers: list

    def __init__(self, set_id: int, used = False):
        self.set_id = set_id
        self.offers = SetScraper(set_id).get_all_sets()
