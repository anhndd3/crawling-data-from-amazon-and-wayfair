from dataclasses import dataclass


@dataclass
class WayFairProduct:
    title: str
    brand: str
    new_price: float
    list_price: str
    rating: str
    rating_count: str
    shipping_fee: str
    sponsored: str


@dataclass
class AmazonProductRanking:
    rank: str
    name: str
    price: float
    url: str


@dataclass
class AmazonProductDetail:
    title: str
    new_price: str
    list_price: float
    rating: str
    rating_count: str
    image_url: str
