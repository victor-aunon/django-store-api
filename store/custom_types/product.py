from typing import Optional, TypedDict


class ProductType(TypedDict, total=False):
    id: int
    pk: Optional[int]
    title: str
    price: float
    category: str
    description: str
    image: str
    amount: int
    rating: float
    rating_count: int
