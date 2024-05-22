from dataclasses import dataclass
import sqlite3
import json
import asyncio
import aiohttp

@dataclass
class Collection:
    set_code: str
    card_num: str

from dataclasses import dataclass

@dataclass
class Card:
    id: str
    oracle_id: str
    tcgplayer_id: int
    cardmarket_id: int
    name: str
    lang: str
    released_at: str
    uri: str
    scryfall_uri: str
    layout: str
    highres_image: bool
    image_status: str
    image_uris: dict[str, str]
    mana_cost: str
    cmc: int
    type_line: str
    oracle_text: str
    colors: list[str]
    color_identity: list[str]
    keywords: list[str]
    legalities: dict[str, str]
    games: list[str]
    reserved: bool
    foil: bool
    nonfoil: bool
    finishes: list[str]
    oversized: bool
    promo: bool
    reprint: bool
    variation: bool
    set_id: str
    set: str
    set_name: str
    set_type: str
    set_uri: str
    set_search_uri: str
    scryfall_set_uri: str
    rulings_uri: str
    prints_search_uri: str
    collector_number: str
    digital: bool
    rarity: str
    flavor_text: str
    card_back_id: str
    artist: str
    artist_ids: list[str]
    illustration_id: str
    border_color: str
    frame: str
    full_art: bool
    textless: bool
    booster: bool
    story_spotlight: bool
    edhrec_rank: int
    penny_rank: int
    prices: dict[str, str]
    related_uris: dict[str, str]
    purchase_uris: dict[str, str]

def get_cards_from_file(file_name):
    code = []
    card = []
    count = 0
    with open(file_name, 'r') as file:
        line = file.readline().rstrip('\n')
        while line:
            items = line.split(',')
            code.append(items[0])
            card.append(items[1])
            line = file.readline().rstrip('\n')
            count += 1
    return code, card, count

async def get_card_data(session, set_code, card_num):
    # Define url and start request
    url = f"https://api.scryfall.com/cards/{set_code}/{card_num}"
    async with session.get(url) as response:
        if response.status == 200:
            json_response = await response.json()
            card = Card(
                id=json_response.get("id", None),
                oracle_id=json_response.get("oracle_id", None),
                tcgplayer_id=json_response.get("tcgplayer_id", None),
                cardmarket_id=json_response.get("cardmarket_id", None),
                name=json_response.get("name", ""),
                lang=json_response.get("lang", ""),
                released_at=json_response.get("released_at", ""),
                uri=json_response.get("uri", ""),
                scryfall_uri=json_response.get("scryfall_uri", ""),
                layout=json_response.get("layout", ""),
                highres_image=json_response.get("highres_image", False),
                image_status=json_response.get("image_status", ""),
                image_uris=json_response.get("image_uris", {}),
                mana_cost=json_response.get("mana_cost", ""),
                cmc=json_response.get("cmc", 0),
                type_line=json_response.get("type_line", ""),
                oracle_text=json_response.get("oracle_text", ""),
                colors=json_response.get("colors", []),
                color_identity=json_response.get("color_identity", []),
                keywords=json_response.get("keywords", []),
                legalities=json_response.get("legalities", {}),
                games=json_response.get("games", []),
                reserved=json_response.get("reserved", False),
                foil=json_response.get("foil", False),
                nonfoil=json_response.get("nonfoil", False),
                finishes=json_response.get("finishes", []),
                oversized=json_response.get("oversized", False),
                promo=json_response.get("promo", False),
                reprint=json_response.get("reprint", False),
                variation=json_response.get("variation", False),
                set_id=json_response.get("set_id", None),
                set=json_response.get("set", ""),
                set_name=json_response.get("set_name", ""),
                set_type=json_response.get("set_type", ""),
                set_uri=json_response.get("set_uri", ""),
                set_search_uri=json_response.get("set_search_uri", ""),
                scryfall_set_uri=json_response.get("scryfall_set_uri", ""),
                rulings_uri=json_response.get("rulings_uri", ""),
                prints_search_uri=json_response.get("prints_search_uri", ""),
                collector_number=json_response.get("collector_number", ""),
                digital=json_response.get("digital", False),
                rarity=json_response.get("rarity", ""),
                flavor_text=json_response.get("flavor_text", ""),
                card_back_id=json_response.get("card_back_id", None),
                artist=json_response.get("artist", ""),
                artist_ids=json_response.get("artist_ids", []),
                illustration_id=json_response.get("illustration_id", None),
                border_color=json_response.get("border_color", ""),
                frame=json_response.get("frame", ""),
                full_art=json_response.get("full_art", False),
                textless=json_response.get("textless", False),
                booster=json_response.get("booster", False),
                story_spotlight=json_response.get("story_spotlight", False),
                edhrec_rank=json_response.get("edhrec_rank", None),
                penny_rank=json_response.get("penny_rank", None),
                prices=json_response.get("prices", {}),
                related_uris=json_response.get("related_uris", {}),
                purchase_uris=json_response.get("purchase_uris", {})
            )
            return card
        elif response.status == 404:
            print(f"Card not found for set_code={set_code}, card_num={card_num}. Skipping.")
            return None
        else:
            print(f"Unexpected status code {response.status} for set_code={set_code}, card_num={card_num}. Skipping.")
            return None
    
def add_collection_db(list_of_cards):
    connection = sqlite3.connect("collection.db")
    cursor = connection.cursor()
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS cards (
        id TEXT,
        oracle_id TEXT,
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

    print("database done")












async def main():
    set_code, card_num, count = get_cards_from_file("cards.txt")
    Cards = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for index in range(count):
            tasks.append(get_card_data(session, set_code[index].lower(), card_num[index]))
            await asyncio.sleep(0.05)

        cards = await asyncio.gather(*tasks)

        for card in cards:
            if card is not None:  # Check if the card data is not None
                print(card.name)
                card_dict = {
                    'id': card.id,
                    'oracle_id': card.oracle_id,
                    'tcgplayer_id': card.tcgplayer_id,
                    'cardmarket_id': card.cardmarket_id,
                    'name': card.name,
                    'lang': card.lang,
                    'released_at': card.released_at,
                    'uri': card.uri,
                    'scryfall_uri': card.scryfall_uri,
                    'layout': card.layout,
                    'highres_image': card.highres_image,
                    'image_status': card.image_status,
                    'image_uris': json.dumps(card.image_uris),
                    'mana_cost': card.mana_cost,
                    'cmc': card.cmc,
                    'type_line': card.type_line,
                    'oracle_text': card.oracle_text,
                    'colors': ', '.join(card.colors),
                    'color_identity': ', '.join(card.color_identity),
                    'keywords': ', '.join(card.keywords),
                    'legalities': json.dumps(card.legalities),
                    'games': ', '.join(card.games),
                    'reserved': card.reserved,
                    'foil': card.foil,
                    'nonfoil': card.nonfoil,
                    'finishes': ', '.join(card.finishes),
                    'oversized': card.oversized,
                    'promo': card.promo,
                    'reprint': card.reprint,
                    'variation': card.variation,
                    'set_id': card.set_id,
                    'set_name': card.set_name,
                    'set_type': card.set_type,
                    'set_uri': card.set_uri,
                    'set_search_uri': card.set_search_uri,
                    'scryfall_set_uri': card.scryfall_set_uri,
                    'rulings_uri': card.rulings_uri,
                    'prints_search_uri': card.prints_search_uri,
                    'collector_number': card.collector_number,
                    'digital': card.digital,
                    'rarity': card.rarity,
                    'flavor_text': card.flavor_text,
                    'card_back_id': card.card_back_id,
                    'artist': card.artist,
                    'artist_ids': ', '.join(card.artist_ids),
                    'illustration_id': card.illustration_id,
                    'border_color': card.border_color,
                    'frame': card.frame,
                    'full_art': card.full_art,
                    'textless': card.textless,
                    'booster': card.booster,
                    'story_spotlight': card.story_spotlight,
                    'edhrec_rank': card.edhrec_rank,
                    'penny_rank': card.penny_rank,
                    'prices': json.dumps(card.prices),
                    'related_uris': json.dumps(card.related_uris),
                    'purchase_uris': json.dumps(card.purchase_uris)
                }
                
                # Call add_collection_db to insert the fetched card into the database
                add_collection_db([card_dict])


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())