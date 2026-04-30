from fastapi import APIRouter
from .. import database, models, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from ..repository import user

router = APIRouter(prefix="/user", tags=["Users"])
get_db = database.get_db


@router.post("/", status_code=201, response_model=schemas.ShowUser)
def create_user(
    request: schemas.User,
    db: Session = Depends(get_db),
):
    return user.create(request, db)


@router.get(
    "/{id}",
    status_code=200,
    response_model=schemas.ShowUser,
)
def get_user(
    id: int,
    db: Session = Depends(get_db),
):
    return user.show(id, db)
