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

#change the port
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8082) #then use python3 main.py

