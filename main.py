from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

app.include_router(auth_router)
app.include_router(order_router)
