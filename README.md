# PIZZA DELIVERY API

This is a REST API for a Pizza delivery service built for fun and learning with FastAPI, SQLAlchemy, and PostgreSQL .

## ROUTES TO IMPLEMENT

| METHOD | ROUTE                                | FUNCTIONALITY              | ACCESS      |
|--------|--------------------------------------|----------------------------|-------------|
| *POST*   | */auth/signup/*                        | *Register new user*          | *All users*   |
| *POST*   | */auth/login/*                         | *Login user*                 | *All users*   |
| *POST*   | */orders/order/*                       | *Place an order*             | *All users*   |
| *PUT*    | */orders/order/update/{order_id}/*     | *Update an order*            | *All users*   |
| *PUT*    | */orders/order/status/{order_id}/*     | *Update order status*        | *Superuser*   |
| *DELETE* | */orders/order/delete/{order_id}/*     | *Delete/Remove an order*     | *All users*   |
| *GET*    | */orders/user/orders/*                 | *Get user's orders*          | *All users*   |
| *GET*    | */orders/orders/*                      | *List all orders made*       | *Superuser*   |
| *GET*    | */orders/orders/{order_id}/*           | *Retrieve an order*          | *Superuser*   |
| *GET*    | */orders/user/order/{order_id}/*       | *Get user's specific order*  | *All users*   |

## How to run the Project

- Install PostgreSQL
- Install Python
- Clone the project with ``` https://github.com/anand-1Abhishek/Pizza_Delivery_App.git  ```
- Create your virtualenv with Pipenv or virtualenv and activate it.
- Install the requirements with pip install -r requirements.txt
- Set Up your PostgreSQL database and set its URI in your database.py
```bash
  engine=create_engine('postgresql://postgres:<username>:<password>@localhost/<db_name>',
    echo=True
)
```
- Create your database by running python init_db.py
- Finally run the API ``` uvicorn main:app ``
  
 
