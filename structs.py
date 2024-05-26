from dataclasses import dataclass

@dataclass
class Card:
    id: str
    oracle_id: str
    multiverse_ids: list[int]
    mtgo_id: int
    mtgo_foil_id: int
    arena_id: int
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
    set_code: str
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