from typing import List
from fastapi import APIRouter

# from blog.oauth2 import get_current_user
from .. import database, models, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response, status
from ..repository import blog

router = APIRouter(prefix="/blog", tags=["Blogs"])
get_db = database.get_db


@router.get("/", response_model=List[schemas.ShowBlog])
def all(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
# @router.post("/blog", status_code=201)
# def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
def create(
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    # user_id: int = int(current_user.id)
    current_user_id = current_user.id  # type: ignore
    return blog.create(request, db, current_user_id)


# def show(id: int, response: Response, db: Session = Depends(get_db)):
@router.get(
    "/single/{id}",
    status_code=200,
    response_model=schemas.ShowBlog,
)
def show(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.show(id, db)


# def show_httpexception(
#     id: int,
#     db: Session = Depends(get_db),
# ):
@router.get("/{id}", status_code=200)
def show_httpexception(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with the id {id} not found",
        )
    return blog


# def destroy(id: int, db: Session = Depends(get_db)):
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.destroy(id, db)


# def update(
#     id: int,
#     request: schemas.Blog,
#     db: Session = Depends(get_db),
# ):
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.update(id, request, db)

    # blog = db.query(models.Blog).filter(models.Blog.id == id)
    #
    # if not blog.first():
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found"
    #     )
    #
    # blog.update(request.dict())
    # db.commit()
    # db.refresh(blog)
    #
    # # or
    # # blog.title = request.title
    # # blog.body = request.body
    # # db.commit()
    # # db.refresh(blog)
    #
    # return "updated"
