from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType
from db.base import Base

class Order(Base):
    __tablename__ = "orders"
    
    ORDER_STATUSES = (
        ('PENDING', 'PENDING'),
        ('IN-TRANSIT', 'IN-TRANSIT'),
        ('DELIVERED', 'DELIVERED')
    )

    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    )
    
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES, impl=String()), default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES, impl=String()), default="SMALL")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="orders")
    
    def __repr__(self):
        return f"<Order {self.id}>"