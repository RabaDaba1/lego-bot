from Scraper import SetScraper
import sqlite3 

def add_set(set_id: int):
    """Adds a new LEGO set to sets table"""

    try:
        conn = sqlite3.connect('./database/database.db')
    except sqlite3.Error as e:
        print('Error connecting to database')
        print(e)

    c = conn.cursor()
    try:
        c.execute(f"""
            INSERT INTO sets (set_id)
            VALUES ({set_id});
        """)
    except sqlite3.IntegrityError as e:
        print(f'Set {set_id} is already in database')
        print(e)
        conn.commit()
    finally:
        conn.close()

def delete_set(set_id: int):
    """Deletes a LEGO set from sets table"""

    try:
        conn = sqlite3.connect('./database/database.db')
    except sqlite3.Error as e:
        print('Error connecting to database')
        print(e)

    c = conn.cursor()
    
    try:
        c.execute(f"""
            DELETE FROM sets
            WHERE set_id = {set_id};
        """)
    except sqlite3.IntegrityError as e:
        print(f'Set {set_id} is not in database')
        print(e)
        conn.commit()
    finally:
        conn.close()


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
