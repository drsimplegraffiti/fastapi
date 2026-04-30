from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import database, models, schemas, token
from ..hashing import Hash
from ..repository import user

router = APIRouter(
    tags=["Authentication"]
)  # if prefix is "/user" ensure you add it to the oauth2
get_db = database.get_db


# def login(request: schemas.Login, db: Session = Depends(get_db)):
@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with {request.username} not found",
        )

    if not Hash.verify(str(user.password), request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"invalid credentials",
        )
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
