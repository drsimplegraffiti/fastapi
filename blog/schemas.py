from typing import List, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


# class ShowBlog(Blog):
#     class Config():
#         orm_mode = True
#
# or


class User(BaseModel):
    # id: int
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    email: str
    name: str

    blogs: List[Blog] = []

    class Config:
        orm_mode = True


# response model
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str 
