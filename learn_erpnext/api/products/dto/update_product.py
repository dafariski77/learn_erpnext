from pydantic import BaseModel, Field


class UpdateProductDto(BaseModel):
    product_id: str = Field(..., min_length=1)
    product_name: str = Field(..., min_length=1)
    description: str = Field(..., max_length=500)
    stock: int = Field(..., ge=0)
    price: int = Field(..., ge=0)

    @classmethod
    def from_request(cls, data: dict) -> "UpdateProductDto":
        return cls(**data)
