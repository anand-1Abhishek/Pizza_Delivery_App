from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class OrderBase(BaseModel):
    quantity: int
    pizza_size: Optional[str] = "SMALL"
    order_status: Optional[str] = "PENDING"

class OrderCreate(OrderBase):
    # Removed total_amount as it will be calculated automatically
    pass

class OrderUpdate(BaseModel):
    quantity: Optional[int] = None
    pizza_size: Optional[str] = None
    order_status: Optional[str] = None
    # Removed total_amount as it will be calculated automatically

class OrderStatusUpdate(BaseModel):
    order_status: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "PENDING"  # Make sure this matches one of the valid choices
            }
        }

class OrderInDBBase(OrderBase):
    id: int
    user_id: int
    total_amount: float  # Included in response but not in request
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "quantity": 2,
                "pizza_size": "LARGE",
                "order_status": "PENDING",
                "total_amount": 37.98,
                "user_id": 1,
                "created_at": "2025-03-02T10:30:00",
                "updated_at": "2025-03-02T10:35:00"
            }
        }

class Order(OrderInDBBase):
    pass