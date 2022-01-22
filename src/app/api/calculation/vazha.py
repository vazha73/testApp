from fastapi import APIRouter
router = APIRouter()

@router.post("/vazha")
async def read_root():
    return {"Hello": "World...11"}
