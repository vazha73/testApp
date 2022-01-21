import datetime
from typing import Optional,List
import datetime as dt
from starlette import status

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()



class Item(BaseModel):
    item_id: int
    q: Optional[str]
    
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}",
    tags=["patients"],
    response_model=Item,
    summary="list of patients",
    response_description="Get list of patients",
    status_code=status.HTTP_201_CREATED)
def read_item(item_id: int, q: str) -> Item:
    return {"item_id": item_id, "q": q}

