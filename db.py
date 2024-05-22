import sqlite3

def add_collection_db(list_of_cards):
    connection = sqlite3.connect("collection.db")
    cursor = connection.cursor()
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS cards (
        id TEXT,
        oracle_id TEXT,
        multiverse_ids TEXT,
        mtgo_id INTEGER,
        mtgo_foil_id INTEGER,
        arena_id INTEGER,
        tcgplayer_id INTEGER,
        cardmarket_id INTEGER,
        name TEXT NOT NULL,
        lang TEXT,
        released_at TEXT,
        uri TEXT,
        scryfall_uri TEXT,
        layout TEXT,
        highres_image BOOLEAN,
        image_status TEXT,
        image_uris TEXT,
        mana_cost TEXT,
        cmc INTEGER,
        type_line TEXT,
        oracle_text TEXT,
        colors TEXT,
        color_identity TEXT,
        keywords TEXT,
        legalities TEXT,
        games TEXT,
        reserved BOOLEAN,
        foil BOOLEAN,
        nonfoil BOOLEAN,
        finishes TEXT,
        oversized BOOLEAN,
        promo BOOLEAN,
        reprint BOOLEAN,
        variation BOOLEAN,
        set_id TEXT,
        set_name TEXT,
        set_type TEXT,
        set_uri TEXT,
        set_search_uri TEXT,
        scryfall_set_uri TEXT,
        rulings_uri TEXT,
        prints_search_uri TEXT,
        collector_number TEXT,
        digital BOOLEAN,
        rarity TEXT,
        flavor_text TEXT,
        card_back_id TEXT,
        artist TEXT,
        artist_ids TEXT,
        illustration_id TEXT,
        border_color TEXT,
        frame TEXT,
        full_art BOOLEAN,
        textless BOOLEAN,
        booster BOOLEAN,
        story_spotlight BOOLEAN,
        edhrec_rank INTEGER,
        penny_rank INTEGER,
        prices TEXT,
        related_uris TEXT,
        purchase_uris TEXT
    );
    '''

    cursor.execute(create_table_sql)
    connection.commit()

    for card in list_of_cards:
        columns = ", ".join(card.keys())  # Dynamically get column names from keys
        placeholders = ", ".join("?" * len(card))  # Generate placeholders
        insert_sql = f"INSERT INTO cards ({columns}) VALUES ({placeholders});"

        # Execute the INSERT statement
        cursor.execute(insert_sql, tuple(card.values()))

    connection.commit()
    connection.close()