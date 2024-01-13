from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProductInfo:
    name: str
    price: Decimal
    brand: str = None
    code: str = None
