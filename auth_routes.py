from fastapi import APIRouter,status
from fastapi.exceptions import HTTPException
from database import Session,engine
from schemas import SignUpModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash 

auth_router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

session=Session(bind=engine)

@auth_router.get('/')
async def hello():
    return {"message" : "Hello World"}



@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    """
    ## Create a user
    This requires the following:
    ```
    username: int
    email: str
    password: str
    is_staff: bool
    is_active: bool
    ```
    """

    # Check if email already exists
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists"
        )

    # Check if username already exists
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists"
        )

    # Create the user
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()

    # Return success message
    return {"message": "User created successfully", "user_name": new_user.username}
