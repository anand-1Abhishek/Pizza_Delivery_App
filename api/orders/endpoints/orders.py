from typing import Any, List, Dict
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from db.deps import get_db, get_current_user, get_current_superuser
from models.order import Order
from models.user import User
from schemas.order import Order as OrderSchema, OrderCreate, OrderUpdate, OrderStatusUpdate

router = APIRouter()

# Helper function to calculate price based on pizza size
def calculate_price(pizza_size: str, quantity: int) -> float:
    # Define base prices for different pizza sizes
    size_prices = {
        "SMALL": 10.99,
        "MEDIUM": 14.99,
        "LARGE": 18.99,
        "EXTRA-LARGE": 22.99
    }
    
    # Get the base price for the selected size (default to SMALL if invalid)
    base_price = size_prices.get(pizza_size, size_prices["SMALL"])
    
    # Calculate total based on quantity
    return round(base_price * quantity, 2)

# Helper function to serialize Order objects for response
def serialize_order(order: Order) -> Dict:
    return {
        "id": order.id,
        "quantity": order.quantity,
        "pizza_size": str(order.pizza_size) if order.pizza_size else "SMALL",
        "order_status": str(order.order_status) if order.order_status else "PENDING",
        "total_amount": order.total_amount,
        "user_id": order.user_id,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    }

@router.post("/order/", response_model=OrderSchema)
def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new order.
    """
    # Calculate the total amount based on pizza size and quantity
    total_amount = calculate_price(order_in.pizza_size, order_in.quantity)
    
    order = Order(
        quantity=order_in.quantity,
        pizza_size=order_in.pizza_size,
        order_status=order_in.order_status,
        total_amount=total_amount,
        user_id=current_user.id
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return serialize_order(order)

# @router.put("/order/update/{order_id}/", response_model=OrderSchema)
# def update_order(
#     *,
#     db: Session = Depends(get_db),
#     order_id: int = Path(...),
#     order_in: OrderUpdate,
#     current_user: User = Depends(get_current_user)
# ) -> Any:
#     """
#     Update an order.
#     """
#     order = db.query(Order).filter(
#         Order.id == order_id, Order.user_id == current_user.id
#     ).first()
    
#     if not order:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Order not found"
#         )
    
#     update_data = order_in.dict(exclude_unset=True)
    
#     # If pizza size or quantity is being updated, recalculate the total amount
#     need_price_update = "pizza_size" in update_data or "quantity" in update_data
    
#     if need_price_update:
#         # Get the new values or use existing ones if not being updated
#         new_size = update_data.get("pizza_size", str(order.pizza_size.value))
#         new_quantity = update_data.get("quantity", order.quantity)
        
#         # Calculate the new total amount
#         update_data["total_amount"] = calculate_price(new_size, new_quantity)
    
#     # Update the order attributes
#     for field, value in update_data.items():
#         setattr(order, field, value)
    
#     db.add(order)
#     db.commit()
#     db.refresh(order)
    
#     return serialize_order(order)

@router.put("/order/status/{order_id}/", response_model=OrderSchema)
def update_order_status(
    *,
    db: Session = Depends(get_db),
    order_id: int = Path(...),
    status_in: OrderStatusUpdate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Update an order's status. Only for superusers.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Get the available choices directly from the model
    valid_statuses = dict(Order.ORDER_STATUSES).keys()
    
    # Normalize the input status to match our choices
    new_status = status_in.order_status.upper()
    
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid order status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    # Use direct SQL update to bypass SQLAlchemy-Utils typing issues
    from sqlalchemy import update
    stmt = update(Order).where(Order.id == order_id).values(order_status=new_status)
    db.execute(stmt)
    db.commit()
    
    # Refresh the order from the database
    order = db.query(Order).filter(Order.id == order_id).first()
    
    return serialize_order(order)

@router.delete("/order/delete/{order_id}/", response_model=OrderSchema)
def delete_order(
    *,
    db: Session = Depends(get_db),
    order_id: int = Path(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete an order.
    """
    order = db.query(Order).filter(
        Order.id == order_id, Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Store the order data before deletion for return
    order_data = serialize_order(order)
    
    db.delete(order)
    db.commit()
    
    return order_data

@router.get("/user/orders/", response_model=List[OrderSchema])
def read_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get all orders for the current user.
    """
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return [serialize_order(order) for order in orders]

@router.get("/orders/", response_model=List[OrderSchema])
def read_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Get all orders. Only for superusers.
    """
    orders = db.query(Order).all()
    return [serialize_order(order) for order in orders]

@router.get("/orders/{order_id}/", response_model=OrderSchema)
def read_order(
    *,
    db: Session = Depends(get_db),
    order_id: int = Path(...),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Get order by ID. Only for superusers.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return serialize_order(order)

@router.get("/user/order/{order_id}/", response_model=OrderSchema)
def read_user_order(
    *,
    db: Session = Depends(get_db),
    order_id: int = Path(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific order for the current user.
    """
    order = db.query(Order).filter(
        Order.id == order_id, Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return serialize_order(order)