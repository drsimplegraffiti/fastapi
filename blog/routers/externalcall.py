import httpx
from fastapi import APIRouter


router = APIRouter(prefix="/external", tags=["External"])



@router.get("/")
async def call_api():
    async with httpx.AsyncClient() as client:
        url = "https://jsonplaceholder.typicode.com/todos/1"
        res = await client.get(url)
    return res.json()
