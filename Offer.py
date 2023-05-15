import pandas as pd

from Scraper import OfferScraper
from Parser import *

class Offer:
    """
    A class to represent an OLX offer

    Attributes:
    -----------
    url: str
        URL of the offer
    offer_id: str
        OLX ID of the offer (last part of the URL)
    set_id: int
        LEGO set number
    date_added: Datetime.date
    date_sold: Datetime.date (default: None)
    title: str
    description: str
    price: str
    is_negotiable: bool
    is_active: bool
    
    Methods:
    --------
    create_list() -> list
        Returns a list with the offer's data
    """

    url: str
    offer_id: str
    set_id: int = None
    date_added: datetime.date = None
    date_sold: datetime.date = None
    title: str = None
    description: str = None
    price: str = None
    is_negotiable: bool = None
    is_active: bool = None

    def __init__(self, url: str):
        scraper = OfferScraper(url)

        self.url = url
        self.offer_id = parse_offer_id(url)
        self.is_active = scraper.is_active()
        self.date_sold = None
        
        if not self.is_active:
            return
        
        # Scrape and parse offer's data
        self.date_added = parse_date(scraper.scrape_date())
        self.title = remove_accents(parse_title(scraper.scrape_title()))
        self.price = parse_price(scraper.scrape_price())
        self.description = remove_accents(parse_description(scraper.scrape_description()))
        self.is_negotiable = (scraper.scrape_negotiable())
        self.set_id = get_set_id(self.title)

    def get_tuple(self) -> tuple:
        return (
            self.offer_id,
            self.url,
            self.set_id,
            self.date_added,
            self.date_sold,
            self.title,
            self.description,
            self.price,
            self.is_negotiable,
            self.is_active
        )
    
    def create_list(self) -> list:
        return list(self.get_tuple())
    