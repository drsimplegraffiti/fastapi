import httpx
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date, datetime
from typing import Any
from typing import Annotated

router = APIRouter(prefix="/tutorial", tags=["Tutorial"])


# see this as dto
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@router.get("/home")
async def read_root():
    return {"Hello": "World"}


@router.get("/hi")
def say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
    return name


@router.post("/dict")
def process_items_dict(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)
    return prices


@router.get("/items/{item_id}")
def read_item(item_id: int | str, q: str | None = None):  # | is called a union
    return {"item_id": item_id, "q": q}


@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


class User(BaseModel):
    id: int
    name: str
    is_tall: bool | None = None
    joined: date


@router.get("/users")
def get_users():

    my_user: User = User(
        id=3,
        name="John Doe",
        is_tall=True,
        joined=date(2018, 7, 19),  # ✅ correct
    )

    second_user_data = {
        "id": 4,
        "name": "Mary",
        "is_tall": True,
        "joined": "2018-11-30",
    }

    my_second_user: User = User(**second_user_data)
    return {"first": my_user, "second": second_user_data}


@router.get("/items")
def get_items(
    item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes, item_any: Any
):
    return item_a, item_b, item_c, item_d, item_e


@router.post("/lists")
def process_items(items: list[str]):
    for item in items:
        print(item)
    return items


class ExternalData(BaseModel):
    id: int
    name: str = "John doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

@router.post("/data")
def data_items(): 
    external_data = {
        "id": "123",
        "signup_ts": "2017-06-01 12:22",
        "friends": [1, "2", b"3"],
    }
    data= ExternalData(**external_data)
    return data



@router.post("/data-annotation")
def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"
