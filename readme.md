

#### Fast api has:
- automatic docs : swagger, redoc
- modern, provides type
- Based on open API, Json Schema
- Http Basic, Oauth2, Headers, Cookies etc
- Dependency Injection
- Uses starlette:
    - websocket, graphql, in-process background tasks
    - startup and shutdown events
- Supports NoSql/Sql databases

#### Setup
https://fastapi.tiangolo.com/

### install fastapi globally or in the virtual env
```bash
#update/upgrade pip

python3 -m venv .venv
source .venv/bin/activate 
python3 -m pip install --upgrade pip

pip3 install fastapi
pip3 install uvicorn
uvicorn --version
```


```python

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"data": {"message": "app is running"}}
```
Run with:
```bash
uvicorn main:app --reload
```

 main in main:app => the file name `main.py`
 app in main:app => the app instance we created from FastAPI()
 .get => operation
 ('/') => path
 @app - path operation decorator
 index => path operation function


 ```python
@app.get("/blog/{id}") #if you pass strings here, you will get:
def show(id: int):
return {"data": id}
```

```bash
{"detail":[{"type":"int_parsing","loc":["path","id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"myblog"}]}
```


```python
# you can also use the str
@app.get("/blog/{id}")
def show(id: str): #str, int, bool is coming from pydantic
    return {"data": id}

```

### swagger:
http://127.0.0.1:8000/docs

### redoc
http://127.0.0.1:8000/redoc



```python

from typing import Optional
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"message": "app is running"}}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}


@app.get("/blogs")
def showquery(
        limit=10, page=1, published: bool = True, sort: Optional[str] = None
):  # by default all queries are required
    if published:
        return {"data": f"from query {published} {page} params {limit}"}
    else:
        return {"data": f"from query {page} params {limit}"}


@app.get("/blog/{id}/comments") #fast api differentiate path variable from query when it sees {}
def comments(id, limit=10): #limit here will be treated as a query params
    return {"data": "comments "}
```


```python

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None
    

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"message": "app is running"}}


@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}


@app.post("/blog")
def create_blog(request: Blog):
    return request


@app.get("/blogs")
def showquery(
    limit=10, page=1, published: bool = True, sort: Optional[str] = None
):  # by default all queries are required
    if published:
        return {"data": f"from query {published} {page} params {limit}"}
    else:
        return {"data": f"from query {page} params {limit}"}


@app.get(
    "/blog/{id}/comments"
)  # fast api differentiate path variable from query when it sees {}
def comments(id):
    return {"data": "comments "}

#change the port, for debugging purpose, dont do in production
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8082) #then use python3 main.py

```


#### Database 
To use database with FastAPI you need SQLAlchemy, a relational mapper and python toolkit
first create `requirements.txt` and add

```txt
fastapi
uvicorn
```

Then use pip3 to install it:
```bash
pip3 install -r requirements.txt
```

__init__.py is used to tell Python that a folder should be treated as a package (i.e., something you can import from).



#### Handling resposne
```python

from fastapi import FastAPI, Depends, status, Response
# or use from schemas import Blog
# from . import schemas
# from . import models

from . import schemas, models
from .database import SessionLocal, engine  # . here mean . → “current package (folder)”
from sqlalchemy.orm import Session


app = FastAPI()

# migrates all the table to the db
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
# @app.post("/blog", status_code=201)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=200)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"blog with id {id} not found"}
    return blog


# run app with uvicorn blog.main:app --reload
```


#### Full crud
```python

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

# or use from schemas import Blog
# from . import schemas
# from . import models
from . import models, schemas
from .database import SessionLocal, engine  # . here mean . → “current package (folder)”

app = FastAPI()

# migrates all the table to the db
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
# @app.post("/blog", status_code=201)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=200)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"blog with id {id} not found"}
    return blog


@app.get("/blog/{id}", status_code=200)
def show_httpexception(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with the id {id} not found",
        )
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == id)
        .delete(synchronize_session=False)
    )
    db.commit()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with the id {id} not found",
        )
    return "done"




@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(get_db),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found"
        )

    blog.update(request.dict())
    db.commit()
    db.refresh(blog)

    # or
    # blog.title = request.title
    # blog.body = request.body
    # db.commit()
    # db.refresh(blog)

    return "updated"


# run app with uvicorn blog.main:app --reload
```


### password hashing install passlib
```bash
pip3 install passlib
# or add to requirements.txt, pip3 install -r requirements.txt


pip uninstall bcrypt -y
pip install bcrypt==4.0.1
```



### password hashing in a single file
```python

from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# or use from schemas import Blog
# from . import schemas
# from . import models
from . import models, schemas
from .database import SessionLocal, engine  # . here mean . → “current package (folder)”

app = FastAPI()

# migrates all the table to the db
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
# @app.post("/blog", status_code=201)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=200, response_model=schemas.ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"blog with id {id} not found"}
    return blog


@app.get("/blog/{id}", status_code=200)
def show_httpexception(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with the id {id} not found",
        )
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == id)
        .delete(synchronize_session=False)
    )
    db.commit()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with the id {id} not found",
        )
    return "done"


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(get_db),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found"
        )

    blog.update(request.dict())
    db.commit()
    db.refresh(blog)

    # or
    # blog.title = request.title
    # blog.body = request.body
    # db.commit()
    # db.refresh(blog)

    return "updated"


pwd_cxt = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

@app.post("/user")
def create_user(
    request: schemas.User,
    db: Session = Depends(get_db),
):

    hashed_password = pwd_cxt.hash(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# run app with uvicorn blog.main:app --reload
```


#### connect to sqlite
if not installed:
```bash
sudo apt install sqlite3
```

```bash
sqlite3 blog.db
# Show tables
.tables
# Exit
.exit

# Make output readable:
.mode column
.headers on
```


```python

from fastapi import APIRouter
from .. import database, models, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from ..hashing import Hash

router = APIRouter(prefix="/user",tags=["Users"])
get_db = database.get_db


@router.post("/", status_code=201, response_model=schemas.ShowUser)
def create_user(
    request: schemas.User,
    db: Session = Depends(get_db),
):

    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/{id}",
    status_code=200,
    response_model=schemas.ShowUser,
)
def get_user(
    id: int,
    db: Session = Depends(get_db),
):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with the id {id} not found",
        )
    return user
```
