from typing import Optional, TypedDict


class ProductRatingType(TypedDict):
    rate: float
    count: int


class ProductType(TypedDict, total=False):
    id: int
    pk: Optional[int]
    title: str
    price: float
    category: str
    description: str
    image: str
    amount: int
    rating: ProductRatingType
