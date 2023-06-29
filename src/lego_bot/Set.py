from .Scraper import SetScraper
from .Offer import Offer
import pandas as pd
from . import db

def add_set(set_id: int):
    """Adds set to database."""
    try:
        db.add_set(set_id)
    except Exception as e:
        print(e)


def delete_set(set_id: int):
    """Deletes set from database."""
    try:
        db.delete_set(set_id)
    except Exception as e:
        print(e)

class Set:
    """
    A class to represent a LEGO set. Constructor scrapes all urls for the set from OLX + urls from database.

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

    def __init__(self, set_id: int, used = False):
        self.set_id = set_id
        
        # Get all urls from OLX
        self.urls = SetScraper(set_id).urls
        # Get all urls from database
        self.urls += db.get_sets_urls(set_id)

        # Remove duplicates
        self.urls = list(set(self.urls))

        self.offers = []
        for url in self.urls:
            try:
                offer = Offer(url)
                if offer.set_id != set_id and offer.is_active:
                    continue
            except Exception as e:
                print(e)
                continue
            except:
                print('Unknown error while creating offer:', url)
                continue
            else:
                self.offers.append(offer)

    def update_db(self):
        db.update_offers(self.set_id, self.offers)
        
    def get_scraped_data(self) -> pd.DataFrame:
        """
        Returns data from scraped offers. Offers with None values in all columns beside ID and url are not active. 
        """
        return pd.DataFrame(
            [offer.get_tuple()[1:] for offer in self.offers],
            index=[offer.offer_id for offer in self.offers],
            columns=['url', 'set_id', 'date_added', 'date_sold', 'title', 'description', 'price', 'is_negotiable', 'is_active']
        )
