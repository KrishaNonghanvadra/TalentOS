from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse

from fastapi import HTTPException

from backend.app.services.auth_service import authenticate_user, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
        "/register",
        response_model = UserResponse,
        status_code = 201
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered."
            )

    hashed_password = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )
    
  

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post(
    "/login",
    response_model = Token
)
def login(
    user_data : UserLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_user(
    db,
    user_data.email,
    user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
    )
    access_token = create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )
    return Token(
        access_token = access_token,
        token_type = "bearer"
    )