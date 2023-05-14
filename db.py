import sqlite3

db_path = './database/database.db'


def set_in_sets(set_id: int) -> bool:
    """Returns True if set is in database, False otherwise"""

    return set_id in get_all_sets()

def set_table_exists(set_id: int) -> bool:
    """Returns True if set table exists, False otherwise"""

    return f'set_{set_id}' in get_all_tables()

def add_set(set_id: int):
    """Adds a new LEGO set to sets table and creates a new table for it"""

    # Check if set is already in database
    if set_in_sets(set_id):
        raise Exception(f'Set {set_id} is already in database')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Add set to sets table
    c.execute(f"""
        INSERT INTO sets (set_id)
        VALUES ({set_id});
    """)

    # Create a new table for the set
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS set_{set_id} (
            id TEXT PRIMARY KEY NOT NULL,
            url TEXT NOT NULL,
            set_id INTEGER,
            date_added TEXT,
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
    in_sets = set_in_sets(set_id)
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

def get_all_sets():
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

def get_all_tables():
    """Prints all tables in database"""

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('SELECT name FROM sqlite_master WHERE type="table"')

    sets = [table[0] for table in c.fetchall()]

    conn.close()

    return sets