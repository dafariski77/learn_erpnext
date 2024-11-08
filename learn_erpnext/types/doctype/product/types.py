from dataclasses import dataclass
from learn_erpnext.types.doctype.base import BaseDocType


@dataclass
class IProduct(BaseDocType):
    product_name: str
    description: str
    stock: int
    price: int
