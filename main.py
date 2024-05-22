from structs import Card
from utils import get_card_data, get_cards_from_file
from db import add_collection_db
import asyncio
import json
import aiohttp




async def main():
    set_code, card_num, count = await get_cards_from_file("cards.txt")
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
                    'multiverse_ids': json.dumps(card.multiverse_ids), 
                    'mtgo_id': card.mtgo_id,  
                    'mtgo_foil_id': card.mtgo_foil_id,  
                    'arena_id': card.arena_id ,
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