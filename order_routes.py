from fastapi import APIRouter, Depends, HTTPException, status
from database import Session, engine
from models import Order, User
from typing import List
from schemas import OrderModel, OrderStatusModel
from auth_routes import get_current_user

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

session = Session(bind=engine)

def get_current_superuser(current_user: User = Depends(get_current_user)):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser privileges required"
        )
    return current_user

@order_router.post('/order/', status_code=status.HTTP_201_CREATED)
async def place_order(order: OrderModel, current_user: User = Depends(get_current_user)):
    """Place a new pizza order"""
    new_order = Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size,
        order_status="PENDING",
        user_id=current_user.id
    )
    
    try:
        session.add(new_order)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {
        "message": "Order created successfully",
        "order": {
            "id": new_order.id,
            "quantity": new_order.quantity,
            "pizza_size": new_order.pizza_size,
            "order_status": new_order.order_status
        }
    }

@order_router.put('/order/update/{order_id}/')
async def update_order(order_id: int, order: OrderModel, current_user: User = Depends(get_current_user)):
    """Update an existing order"""
    db_order = session.query(Order).filter(Order.id == order_id).first()
    
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    if db_order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own orders"
        )
    
    if db_order.order_status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending orders can be updated"
        )
    
    db_order.quantity = order.quantity
    db_order.pizza_size = order.pizza_size
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {"message": "Order updated successfully"}

@order_router.put('/order/status/{order_id}/')
async def update_order_status(
    order_id: int, 
    order_status: OrderStatusModel, 
    current_user: User = Depends(get_current_superuser)
):
    """Update order status (Superuser only)"""
    db_order = session.query(Order).filter(Order.id == order_id).first()
    
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    db_order.order_status = order_status.order_status
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {"message": "Order status updated successfully"}

@order_router.delete('/order/delete/{order_id}/')
async def delete_order(order_id: int, current_user: User = Depends(get_current_user)):
    """Delete an order"""
    db_order = session.query(Order).filter(Order.id == order_id).first()
    
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    if db_order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own orders"
        )
    
    try:
        session.delete(db_order)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {"message": "Order deleted successfully"}

@order_router.get('/user/orders/')
async def get_user_orders(current_user: User = Depends(get_current_user)):
    """Get all orders for the current user"""
    user_orders = session.query(Order).filter(Order.user_id == current_user.id).all()
    return user_orders

@order_router.get('/orders/')
async def list_all_orders(current_user: User = Depends(get_current_superuser)):
    """List all orders (Superuser only)"""
    orders = session.query(Order).all()
    return orders

@order_router.get('/orders/{order_id}/')
async def retrieve_order(order_id: int, current_user: User = Depends(get_current_superuser)):
    """Retrieve a specific order (Superuser only)"""
    order = session.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    return order

@order_router.get('/user/order/{order_id}/')
async def get_user_specific_order(order_id: int, current_user: User = Depends(get_current_user)):
    """Get a specific order for the current user"""
    order = session.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    return order