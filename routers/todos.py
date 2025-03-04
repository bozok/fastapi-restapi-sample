from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Todos
from database import SessionLocal

from .auth import get_current_user



router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.user_id == user.get('user_id')).all()


@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.pkid == todo_id).filter(Todos.user_id == user.get('user_id')).first()
    if todo_model:
        return todo_model

    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post('/', status_code=status.HTTP_201_CREATED)
def new_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    todo_model = Todos(**todo_request.model_dump(), user_id=user.get('user_id'))
    print(user)

    db.add(todo_model)
    db.commit()


@router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.pkid == todo_id).filter(Todos.user_id == user.get('user_id')).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail='Todo not found.')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.pkid == todo_id).filter(Todos.user_id == user.get('user_id')).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail='Todo not found.')

    db.query(Todos).filter(Todos.pkid == todo_id).filter(Todos.user_id == user.get('user_id')).delete()
    db.commit()
