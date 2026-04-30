from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token

from sqlalchemy.orm import Session
from . import database, models, schemas, oauth2

get_db = database.get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # this points to the login route

# def get_current_user(data: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     return token.verify_token(data, credentials_exception)


def get_current_user(
    token_str: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = token.verify_token(token_str, credentials_exception)

    user = db.query(models.User).filter(models.User.email == token_data.email).first()

    if not user:
        raise credentials_exception

    return user  # ✅ now returns full user object
