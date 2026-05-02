

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

#### Build cli using Typer
https://typer.tiangolo.com/

#### Fast api uses: 
- starlette: for web servers, https://www.starlette.dev/
    - Starlette is designed to be used either as a complete framework, or as an ASGI toolkit.
    - Starlette is a lightweight ASGI framework/toolkit, which is ideal for building async web services in Python.
- pydantic: Build and validate data with Pydantic Validation



### use 
```bash
fastapi dev # to run instead of uvivorn or use `fastapi run`
# ensure to install "fastapi[standard]" in your requirements .txt
```
The command fastapi dev reads your main.py file automatically, detects the FastAPI app in it, and starts a server using Uvicorn.
By default, fastapi dev will start with auto-reload enabled for local development.


#### deploy
```bash
fastapi deploy
```

### standard Dependencies¶
When you install FastAPI with pip install "fastapi[standard]" it comes with the standard group of optional dependencies:

Used by Pydantic:
    email-validator - for email validation.

Used by Starlette:
    httpx - Required if you want to use the TestClient.
    jinja2 - Required if you want to use the default template configuration.
    python-multipart - Required if you want to support form "parsing", with request.form().

Used by FastAPI:
    uvicorn - for the server that loads and serves your application. This
    includes uvicorn[standard], which includes some dependencies (e.g. uvloop)
    needed for high performance serving.

    fastapi-cli[standard] - to provide the fastapi command.
        This includes fastapi-cloud-cli, which allows you to deploy your FastAPI application to FastAPI Cloud.

### Without standard Dependencies¶
If you don't want to include the standard optional dependencies, you can
install with pip install fastapi instead of pip install "fastapi[standard]".
Without fastapi-cloud-cli¶

If you want to install FastAPI with the standard dependencies but without the
fastapi-cloud-cli, you can install with pip install
"fastapi[standard-no-fastapi-cloud-cli]".

FastAPI is actually a sub-class of Starlette. 

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


#### Env variable
💬 You could create an env var MY_NAME with
export MY_NAME="Wade Wilson"

💬 Then you could use it with other programs, like
echo "Hello $MY_NAME"

Hello Wade Wilson

### Read env in python
```python
import os

name = os.getenv("MY_NAME", "WORLD")
print(f"hello ${name}")
```

```python
💬 Here we don't set the env var yet
python main.py

💬 As we didn't set the env var, we get the default value

Hello World from Python

💬 But if we create an environment variable first
export MY_NAME="Wade Wilson"

💬 And then call the program again
python main.py

💬 Now it can read the environment variable

Hello Wade Wilson from Python
```



#### virtual envs
create using venv module:
python -m venv .venv

create using uv
uv venv

### activate virtual env
linux/macos: source .venv/bin/activate
windows powershell: .venv\Scripts\Activate.ps1
windows bash: source .venv/Scripts/activate

### check if virtual env is active
```bash
which python ##mac and linux
Get-Command python #windows
```

```bash
~/Downloads/fastapi-env main wip ❯ which python                                                                                                                    4s   fastapi-env   system
/usr/bin/python
~/Downloads/fastapi-env main wip ❯ source .venv/bin/activate                                                                                                            fastapi-env   system

~/Downloads/fastapi-env main wip ❯ which python                                                                                                                         fastapi-env   system
/home/xybug/Downloads/fastapi-env/.venv/bin/python
```

#### upgrade pip
If you use uv you would use it to install things instead of pip, so you don't need to upgrade pip. 
If you are using pip to install packages (it comes by default with Python), you
should upgrade it to the latest version.
Many exotic errors while installing a package are solved by just upgrading pip first.

#### upgrade pip command
```bash
source .venv/bin/activate 
python -m pip install --upgrade pip
```

Sometimes, you might get a No module named pip error when trying to upgrade pip.
If this happens, install and upgrade pip using the command below:
```bash
python -m ensurepip --upgrade
```


### Add .gitignore
If you are using Git (you should), add a .gitignore file to exclude everything in your .venv from Git.
If you used uv to create the virtual environment, it already did this for you, you can skip this step. 
Do this once, right after you create the virtual environment.
```bash
echo "*" > .venv/.gitignore
```

### Install packages directly
If you're in a hurry and don't want to use a file to declare your project's
package requirements, you can install them directly.

Note: It's a (very) good idea to put the packages and versions your program
needs in a file (for example requirements.txt or pyproject.toml).

using uv:
```bash
uv pip install "fastapi[standard]"
```
using pip:
```bash
pip install "fastapi[standard]"
```

### Install from requirements.txt¶
pip:
```bash
pip install -r requirements.txt
```
uv:
```bash
uv pip install -r requirements.txt
```

A requirements.txt with some packages could look like:
```bash
fastapi[standard]==0.113.0
pydantic==2.8.0
```


### Run Your Program¶

After you activated the virtual environment, you can run your program, and it
will use the Python inside of your virtual environment with the packages you
installed there.
```bash
python main.py
Hello World
```

### Activating path
Activating a virtual environment adds its path .venv/bin (on Linux and macOS)
    or .venv\Scripts (on Windows) to the PATH environment variable.

### Why deactivate
But if you deactivate the virtual environment and activate the new one for
project A then when you run python it will use the Python from the
virtual environment in projectB.


### Installing FastApi
```bash

pip install "fastapi[standard]" # if you want default optional standard
dependencies, including fastapi-cloud-cli, which allows you to deploy to
FastAPI Cloud

pip install fastapi
If you don't want to have those optional dependencies

If you want to install the standard dependencies but without the
fastapi-cloud-cli, you can install with pip install
"fastapi[standard-no-fastapi-cloud-cli]".
```

#### Create a simple server
Create a file named `sandbox.py`
```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def home():
    return "hi"
```

run with:
```bash
fastapi run sandbox.py
# fastapi dev
```


### Configure the app entrypoint in pyproject.toml¶
You can configure where your app is located in a pyproject.toml file like:

```toml
[tool.fastapi]
entrypoint = "main:app"
```
If your code was structured like:
.
├── backend
│   ├── main.py
│   ├── __init__.py

Then you would set the entrypoint as:
```toml
[tool.fastapi]
entrypoint = "backend.main:app"
```

### When you declare other functions parameters that are not part of the path parameters,
they are automatically interpreted as "query" parameter
```python
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10, q: str | None = None):
    return f"{fake_items_db[skip : skip + limit]} and q is {q}"
```


### request body
```python
```
