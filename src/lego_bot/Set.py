from matplotlib import pyplot as plt
import seaborn as sns
from tqdm import tqdm
import pandas as pd
import datetime

from .Scraper import SetScraper
from .Offer import Offer
from . import database

def add_set(set_id: int):
        """Adds set to database."""
        try:
            database.add_set(set_id)
        except Exception as e:
            print(e)


def delete_set(set_id: int):
    """Deletes set from database."""
    try:
        database.delete_set(set_id)
    except Exception as e:
        print(e)
class Set:
    """
    A class to represent a LEGO set.

    Attributes:
    -----------
    set_id: int
        LEGO set number
    urls: list
        List of urls to each offer for the LEGO set
    offers: list[Offer]
        List of offers for the LEGO set
    """
    set_id: int
    urls: list
    offers: list[Offer]

    def __init__(self, set_id: int, scrape_and_update_db = True):
        self.set_id = set_id
        
        if not database.set_in_db(self.set_id):
            add_set(self.set_id)
            
        if scrape_and_update_db:
            print("Scraping offers from OLX")
            print("--------------------------------------")
            self.scrape()
            
            print("\nUpdating database")
            print("--------------------------------------")
            self.update_db()

    def update_db(self):
        """Updates database with scraped offers."""
        database.update_offers(self.set_id, self.offers)
        
    def scrape(self):
        """Scrapes all offers data from OLX + urls from database for particular LEGO set."""
        
        # Get all urls from OLX and database
        self.urls = SetScraper(self.set_id).urls
        self.urls += database.get_sets_urls(self.set_id)

        # Remove duplicates
        self.urls = list(set(self.urls))

        self.offers = []
        not_added_offers = [] # Offer urls listing multiple sets
        for url in tqdm(self.urls):
            try:
                offer = Offer(url)
                if offer.set_id != self.set_id and offer.is_active:
                    not_added_offers.append(offer)
                    continue
            except Exception as e:
                if e.args[0] == 'More than one set ID found':
                    not_added_offers.append(url)
                continue
            except:
                print('Unknown error while creating offer:', url)
                continue
            else:
                self.offers.append(offer)
                
        print('\033[93m' + f"Skipped {len(not_added_offers)} offers that listed multiple sets" + '\033[0m')
        print('\033[92m' + f"Scraped {len(self.offers)} offers" + '\033[0m')
        
    def get_scraped_data(self) -> pd.DataFrame:
        """
        Returns data from scraped offers. Offers with None values in all columns beside ID and url are not active. 
        """
        return pd.DataFrame(
            [offer.get_tuple() for offer in self.offers],
            columns=['offer_id','url', 'set_id', 'date_added', 'date_sold', 'title', 'description', 'price', 'is_negotiable', 'is_active']
        ).set_index('offer_id')
        
    def get_db_data(self) -> pd.DataFrame:
        """Returns all offer from database for particular LEGO set."""
        offers = database.get_offers(self.set_id)
        df = pd.DataFrame(data=offers, columns=['offer_id', 'url', 'set_id', 'date_added', 'date_sold', 'title', 'description', 'price', 'is_negotiable', 'is_active'])
        
        df.set_index('offer_id', inplace=True)
        
        df['date_added'] = pd.to_datetime(df['date_added'])
        df['date_sold'] = pd.to_datetime(df['date_sold'])
        
        return df

    def get_sold_offers(self) -> pd.DataFrame:
        """Returns all sold offers from database for particular LEGO set."""
        database_df = self.get_db_data()
        filtr = database_df['date_sold'].notnull()

        sold_offers = database_df[filtr]
        
        return sold_offers

    def plot_trend(self):
        """Plots regression plot of sold offers price over time."""
        sold_offers = self.get_sold_offers()
        
        sold_offers['date_sold_seconds'] = sold_offers['date_sold'].apply(lambda x: x.timestamp())
        ax1 = sns.regplot(x='date_sold_seconds', y='price', data=sold_offers)
        ax1.set(title=f'Price trend for set {self.set_id}', xlabel='Date sold', ylabel='Price')

        ax2 = plt.gca()
        xticks = ax2.get_xticks()
        xticks_dates = [datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d') for x in xticks]
        ax2.set_xticklabels(xticks_dates)