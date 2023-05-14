from Scraper import SetScraper
import db
import sqlite3 

def add_set(set_id: int):
    db.add_set(set_id)


def delete_set(set_id: int):
    db.delete_set(set_id)

class Set:
    """
    A class to represent a LEGO set

    Attributes:
    -----------
    set_id: int
        LEGO set number
    offers: list
        List of OLX offers for the LEGO set
    """
    set_id: int
    offers: list

    def __init__(self, set_id: int, used = False):
        self.set_id = set_id
        self.offers = SetScraper(set_id).get_all_sets()
