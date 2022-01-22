from fastapi import APIRouter
from typing import Optional,List
from starlette import status
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    item_id: int
    q: Optional[str]


router = APIRouter()
    
@router.get("/")
async def read_root():
    return {"Hello": "World."}

@router.get("/test")
async def read_root():
    return {"Test": "test2"}

@router.get("/items/{item_id}",
    tags=["read_item"],
    response_model=Item,
    summary="list of patients",
    response_description="Get list of patients",
    status_code=status.HTTP_201_CREATED)
async def read_item(item_id: int, q: str) -> Item:
    return {"item_id": item_id, "q": q}
