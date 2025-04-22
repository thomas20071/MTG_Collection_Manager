import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("mtg_cards.db")
cursor = conn.cursor()

# Create tables
schema_sql = [
    """
    CREATE TABLE IF NOT EXISTS Sets (
        set_id INTEGER PRIMARY KEY AUTOINCREMENT,
        set_name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL,
        release_date DATE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS CardTypes (
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT UNIQUE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Cards (
        card_id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_name TEXT NOT NULL,
        mana_cost TEXT,
        cmc INTEGER,
        power TEXT,
        toughness TEXT,
        loyalty INTEGER,
        rarity TEXT CHECK(rarity IN ('Common', 'Uncommon', 'Rare', 'Mythic')),
        set_id INTEGER,
        type_line TEXT,
        oracle_text TEXT,
        flavor_text TEXT,
        artist TEXT,
        image_url TEXT,
        FOREIGN KEY (set_id) REFERENCES Sets(set_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Card_CardTypes (
        card_id INTEGER,
        type_id INTEGER,
        PRIMARY KEY (card_id, type_id),
        FOREIGN KEY (card_id) REFERENCES Cards(card_id),
        FOREIGN KEY (type_id) REFERENCES CardTypes(type_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS CardColors (
        color_id INTEGER PRIMARY KEY AUTOINCREMENT,
        color_name TEXT UNIQUE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Card_CardColors (
        card_id INTEGER,
        color_id INTEGER,
        PRIMARY KEY (card_id, color_id),
        FOREIGN KEY (card_id) REFERENCES Cards(card_id),
        FOREIGN KEY (color_id) REFERENCES CardColors(color_id)
    );
    """
]

# Execute each table creation statement
for sql in schema_sql:
    cursor.execute(sql)

# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ MTG card database created successfully (mtg_cards.db)")
