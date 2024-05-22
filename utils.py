import json
import asyncio
import aiohttp
import aiofiles
from structs import Card
from functools import lru_cache


async def get_cards_from_file(file_name):
    code = []
    card = []
    count = 0
    async with aiofiles.open(file_name, mode='r') as file:
        async for line in file:
            line = line.rstrip('\n')
            if line:
                items = line.split(",")
                code.append(items[0])
                card.append(items[1])
                count += 1
    return code, card, count




@lru_cache(maxsize=512)
async def get_card_data(session, set_code, card_num):
    # Define url and start request
    url = f"https://api.scryfall.com/cards/{set_code}/{card_num}"
    async with session.get(url) as response:
        if response.status == 200:
            json_response = await response.json()
            card = Card(
                id=json_response.get("id", None),
                oracle_id=json_response.get("oracle_id", None),
                multiverse_ids = json_response.get("multiverse_ids", []),
                mtgo_id = json_response.get("mtgo_id", None),
                mtgo_foil_id = json_response.get("mtgo_foil_id", None),
                arena_id = json_response.get("arena_id", None),
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