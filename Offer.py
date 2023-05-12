import pandas as pd

from Scraper import OfferScraper
from Parser import *

class Offer:
    url: str
    title: str
    price: float
    description: str
    is_negotiable: bool
    is_active: bool
    set_id: int

    # Constructor
    def __init__(self, url: str):
        scraper = OfferScraper(url)

        self.url = url
        self.is_active = scraper.is_active()
        
        if not self.is_active:
            return
        
        # Parse offer's data
        self.title = parse_title(scraper.scrape_title())
        self.price = parse_price(scraper.scrape_price())
        self.description = parse_description(scraper.scrape_description())
        self.is_negotiable = (scraper.scrape_negotiable())
        self.set_id = get_set_id(self.title)

    # Method to create list from offer's data
    def create_list(self) -> list:
        return [
            self.url,
            self.set_id,
            self.title,
            self.description,
            self.price,
            self.is_negotiable,
            self.is_active
        ]