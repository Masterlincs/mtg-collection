from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, Table, MetaData, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from structs import Card  
from dataclasses import asdict
import json

# Setup SQLAlchemy
DATABASE_URI = 'sqlite:///collection.db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Define the Base and Card Model
Base = declarative_base()

class CardModel(Base):
    __tablename__ = 'cards'
    id = Column(String, primary_key=True)
    oracle_id = Column(String)
    multiverse_ids = Column(JSON)
    mtgo_id = Column(Integer)
    mtgo_foil_id = Column(Integer)
    arena_id = Column(Integer)
    tcgplayer_id = Column(Integer)
    cardmarket_id = Column(Integer)
    name = Column(String, nullable=False)
    lang = Column(String)
    released_at = Column(String)
    uri = Column(String)
    scryfall_uri = Column(String)
    layout = Column(String)
    highres_image = Column(Boolean)
    image_status = Column(String)
    image_uris = Column(JSON)
    mana_cost = Column(String)
    cmc = Column(Integer)
    type_line = Column(String)
    oracle_text = Column(String)
    colors = Column(JSON)
    color_identity = Column(JSON)
    keywords = Column(String)
    legalities = Column(JSON)
    games = Column(JSON)
    reserved = Column(Boolean)
    foil = Column(Boolean)
    nonfoil = Column(Boolean)
    finishes = Column(JSON)
    oversized = Column(Boolean)
    promo = Column(Boolean)
    reprint = Column(Boolean)
    variation = Column(Boolean)
    set_id = Column(String)
    set_code = Column(String)
    set_name = Column(String)
    set_type = Column(String)
    set_uri = Column(String)
    set_search_uri = Column(String)
    scryfall_set_uri = Column(String)
    rulings_uri = Column(String)
    prints_search_uri = Column(String)
    collector_number = Column(String)
    digital = Column(Boolean)
    rarity = Column(String)
    flavor_text = Column(String)
    card_back_id = Column(String)
    artist = Column(String)
    artist_ids = Column(JSON)
    illustration_id = Column(String)
    border_color = Column(String)
    frame = Column(String)
    full_art = Column(Boolean)
    textless = Column(Boolean)
    booster = Column(Boolean)
    story_spotlight = Column(Boolean)
    edhrec_rank = Column(Integer)
    penny_rank = Column(Integer)
    prices = Column(JSON)
    related_uris = Column(JSON)
    purchase_uris = Column(JSON)

# Create tables
Base.metadata.create_all(engine)

def add_collection_db(list_of_cards):
    """
    Adds a list of cards to the database.
    :param list_of_cards: List of dictionaries representing cards to be added.
    """
    for card_data in list_of_cards:
        card_model = CardModel(**card_data)
        session.add(card_model)
    session.commit()