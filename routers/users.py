from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Users
from database import SessionLocal

from .auth import get_current_user, bcrypt_context



router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone_number: str | None


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get('/', status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.pkid == user.get('user_id')).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    user_response = UserModel(username=user_model.username, email=user_model.email, first_name=user_model.first_name, last_name=user_model.last_name, role=user_model.role, phone_number=user_model.phone_number)
    return user_response


@router.put('/change-password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.pkid == user.get('user_id')).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password change')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()


@router.put('/phone-number/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.pkid == user.get('user_id')).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()


