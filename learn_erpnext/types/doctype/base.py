from dataclasses import dataclass


@dataclass
class BaseDocType:
    name: str
    owner: str
    creation: str
    modified: str
    modified_by: str
    docstatus: int
    idx: int


@dataclass
class IProduct(BaseDocType):
    product_name: str
    description: str
    stock: int
    price: int
