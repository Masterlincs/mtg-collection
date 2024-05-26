from structs import Card
from utils import get_card_data, get_cards_from_file
from db import add_collection_db
from dataclasses import asdict
import asyncio
import json
import aiohttp
from flask import Flask





async def fetch_and_store_cards():
    set_codes, card_nums = await get_cards_from_file("cards.txt")
    async with aiohttp.ClientSession() as session:
        tasks = []
        for set_code, card_num in zip(set_codes, card_nums):
            tasks.append(get_card_data(session, set_code.lower(), card_num))
        cards = await asyncio.gather(*tasks)

        for card in cards:
            if card is not None:  # Check if the card data is not None
                card_dict = asdict(card)  # Convert Card dataclass instance to dictionary
                # Prepare the list of cards to be inserted into the database
                cards_to_insert = [card_dict]
                # Call add_collection_db to insert the fetched card into the database
                add_collection_db(cards_to_insert)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(fetch_and_store_cards())