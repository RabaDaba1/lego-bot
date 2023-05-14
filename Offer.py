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
    id: str
        OLX ID of the offer (last part of the URL)
    title: str
    description: str
    price: str
    is_negotiable: bool
    is_active: bool
    set_id: int
        LEGO set number
    
    Methods:
    --------
    create_list() -> list
        Returns a list with the offer's data
    """

    def __init__(self, url: str):
        scraper = OfferScraper(url)

        self.url = url
        self.id = parse_id(url)
        self.is_active = scraper.is_active()
        
        if not self.is_active:
            return
        
        # Parse offer's data
        self.title = parse_title(scraper.scrape_title())
        self.price = parse_price(scraper.scrape_price())
        self.description = parse_description(scraper.scrape_description())
        self.is_negotiable = (scraper.scrape_negotiable())
        self.set_id = get_set_id(self.title)

    def create_list(self) -> list:
        return [
            self.url,
            self.id,
            self.set_id,
            self.title,
            self.description,
            self.price,
            self.is_negotiable,
            self.is_active
        ]