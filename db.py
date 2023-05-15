import sqlite3
from datetime import date, datetime
from Offer import Offer

db_path = './database/database.db'

#--------------------#
#-Checking functions-#
#--------------------#
def set_in_db(set_id: int) -> bool:
    """Returns True if set is in database, False otherwise"""

    return set_id in get_all_sets()

def set_table_exists(set_id: int) -> bool:
    """Returns True if set table exists, False otherwise"""

    return f'set_{set_id}' in get_all_tables()

def offer_in_db(offer_id: str, set_id: int = None) -> int:
    """Returns True if offer is in database, False otherwise"""
    offer = get_offer(offer_id, set_id)

    return True if offer else False

#--------------------------------#
#-Functions for editing database-#
#--------------------------------#
def add_set(set_id: int):
    """Adds a new LEGO set to sets table and creates a new table for it"""

    # Check if set is already in database
    if set_in_db(set_id):
        raise Exception(f'Set {set_id} is already in database')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Add set to 'sets' table
    c.execute(f"""
        INSERT INTO sets (set_id)
        VALUES ({set_id});
    """)

    # Create a new table for the set
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS set_{set_id} (
            offer_id TEXT PRIMARY KEY NOT NULL,
            url TEXT NOT NULL,
            set_id INTEGER,
            date_added TEXT,
            date_sold TEXT,
            title TEXT,
            description TEXT,
            price REAL,
            is_negotiable INTEGER,
            is_active INTEGER NOT NULL
        );""")

    conn.commit()
    conn.close()

    print(f'Set {set_id} added to database') 

def delete_set(set_id: int):
    """Deletes a LEGO set from sets table and deletes its table"""
    in_sets = set_in_db(set_id)
    table_exists = set_table_exists(set_id)

    # Check if set is in database
    if not in_sets and not table_exists:
        raise Exception(f'Set {set_id} is not in database')
    
    conn = sqlite3.connect('./database/database.db')
    c = conn.cursor()

    if in_sets:
        # Delete set from 'sets' table
        c.execute(f"""
            DELETE FROM sets
            WHERE set_id = {set_id};
        """)

    if table_exists:
        # Delete set table
        c.execute(f"""
            DROP TABLE set_{set_id};
        """)

    conn.commit()
    conn.close()

    print(f'Set {set_id} deleted from database')

def add_offer(offer: Offer):
    """Adds an offer to a its set table"""

    # Check if offer has a set_id
    if not offer.set_id:
        raise Exception('Passed Offer object has a set_id of None')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # If offer is not in database, add it
    if not offer_in_db(offer.offer_id, offer.set_id):
        c.execute(f"""
            INSERT INTO set_{offer.set_id} (
                offer_id,
                url,
                set_id,
                date_added,
                date_sold,
                title,
                description,
                price,
                is_negotiable,
                is_active
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            offer.get_tuple()
        )

        conn.commit()
        conn.close()
    else:
        conn.close()
        raise Exception(f'Offer {offer.offer_id} is already in database in table set_{offer.set_id}')

#-------------------------------#
#-Functions for retrieving data-#
#-------------------------------#
def get_offer(offer_id: int, set_id: int = None) -> tuple:
    """Returns an offer tuple from database"""

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    offer = tuple()

    if set_id and not set_in_db(set_id):
        raise Exception(f'Set number {set_id} is not in database')

    # If set_id is passed, search only that set table
    if set_id:
        c.execute(f"""
            SELECT *
            FROM set_{set_id}
            WHERE offer_id = ?;
            """,
            (offer_id, )
        )

        offer = c.fetchone()
    else:
        # If set_id is not passed, search all set tables
        tables = get_set_tables()

        for table in tables:
            c.execute(f"""
                SELECT *
                FROM {table}
                WHERE offer_id = ?;
                """,
                (offer_id, )
            )

            offer = c.fetchone()
            if offer:
                break

    conn.close()

    return offer or tuple()

def get_all_sets() -> list[int]:
    """Returns a list of all sets in sets table"""

    conn = sqlite3.connect('./database/database.db')
    c = conn.cursor()

    c.execute(f"""
        SELECT set_id
        FROM sets;
    """)

    sets = [set_id[0] for set_id in c.fetchall()]
    conn.close()
    
    return sets

def get_all_tables() -> list[str]:
    """Prints all tables in database"""

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('SELECT name FROM sqlite_master WHERE type="table"')

    sets = [table[0] for table in c.fetchall()]

    conn.close()

    return sets

def get_set_tables() -> list[str]:
    """Returns a list of all set tables in database"""

    tables = get_all_tables()
    
    return [table for table in tables if table.startswith('set_')]

def get_offers(set_id: int) -> list[tuple]:
    """Returns a list of all offers for a set"""

    # Check if set is in database
    if not set_in_db(set_id):
        raise Exception(f'Set {set_id} is not in database')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(f"""
        SELECT *
        FROM set_{set_id};
    """)

    offers = []
    for offer in c.fetchall():
        offers.append(offer)

    conn.close()

    return offers

def get_sets_urls(set_id: int) -> list[str]:
    """Returns a list of all offer URLs from a database table for a set"""

    # Check if set is in database
    if not set_in_db(set_id):
        raise Exception(f'Set number {set_id} is not in database')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(f"""
        SELECT url
        FROM set_{set_id};
    """)

    urls = [url[0] for url in c.fetchall()]

    conn.close()

    return urls

def get_table_column_names(table: str) -> list[str]:
    """Returns a list of all column names in a table"""

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(f"""
        PRAGMA table_info({table});
    """)

    columns = [column[1] for column in c.fetchall()]

    conn.close()

    return columns

def get_set_id(offer_id: str) -> int:
    """Returns set_id if offer is in database, None otherwise"""
    offer = get_offer(offer_id)
    return offer[2] if offer else None

#---------------------------------#
#-Functions for updating database-#
#---------------------------------#
def update_offers(set_id: int, offers: list[Offer]):
    """Updates offers in database for specified set"""

    # Check if set is in database
    if not set_in_db(set_id):
        raise Exception(f'Set {set_id} is not in database')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for offer in offers:
        # 1) If offer is not in database, add it
        try:
            add_offer(offer, set_id)
        except Exception as e:
            # Catch exception if offer is already in database
            pass
        else:
            print(f'New offer {offer.offer_id} added to database to set_{set_id}')
            continue

        # 2) If offer is in database, check if it needs to be updated
        # Get offers date_added
        c.execute(f"""
            SELECT date_added
            FROM set_{set_id}
            WHERE offer_id = ?;
            """,
            (offer.offer_id, )
        )
        date_added = datetime.strptime(c.fetchone()[0], '%Y-%m-%d').date()

        # Get offers is_active
        c.execute(f"""
            SELECT is_active
            FROM set_{set_id}
            WHERE offer_id = ?;
            """,
            (offer.offer_id, )
        )
        is_active = c.fetchone()[0]

        # If offer expired
        if not offer.is_active and is_active and date.today() - date_added >= 30:
            c.execute(f"""
                    UPDATE set_{set_id}
                    SET
                        is_active = 0
                    WHERE offer_id = ?
                    """,
                    (offer.offer_id, )
            )
            
            print(f'Offer expired: {offer.url}')
        # If offer got sold
        elif is_active and not offer.is_active:
            c.execute(f"""
                UPDATE set_{set_id}
                SET
                    date_sold = ?,
                    is_active = ?
                WHERE offer_id = ?
                """,
                (date.today().isoformat(), offer.is_active, offer.offer_id)
            )

            print(f'Offer sold: {offer.url}')
        # If offer got reactivated
        elif not is_active and offer.is_active:
            c.execute(f"""
                UPDATE set_{set_id}
                SET
                    date_sold = NULL,
                    is_active = ?
                WHERE offer_id = ?
                """,
                (offer.is_active, offer.offer_id)
            )

            print(f'Offer reactivated: {offer.url}')
        # If offer is active and not sold
        elif is_active and offer.is_active:
            c.execute(f"""
                UPDATE set_{set_id}
                SET
                    url = ?,
                    set_id = ?,
                    date_sold = ?,
                    title = ?,
                    description = ?,
                    price = ?,
                    is_negotiable = ?,
                    is_active = ?
                WHERE offer_id = ?
                """,
                (offer.url, offer.set_id, offer.date_sold, offer.title, offer.description, offer.price, offer.is_negotiable, offer.is_active, offer.offer_id)
            )

    conn.commit()
    conn.close()

    print(f'Offers for set {set_id} updated')