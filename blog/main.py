from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, authentication, externalcall, tutorial

app = FastAPI()

# migrates all the table to the db
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(externalcall.router)
app.include_router(tutorial.router)

# run app with uvicorn blog.main:app --reload
