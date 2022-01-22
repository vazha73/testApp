from fastapi import APIRouter
router = APIRouter()

@router.get("/giorgi/calculator/")
async def read_root(a: int, b: int, op: str):
    # using anonymous functions to define operators
    operators = {"plus": (lambda a,b: a+b), "minus": (lambda a,b: a-b), "multiply": (lambda a,b: a*b), "divide": (lambda a,b: a/b)}
    if op not in operators.keys():
        return {"error": "operator unknown. use (plus, minus, multiply, divide)."}

    try:
        return operators[op] (a, b)
    except ZeroDivisionError:
        return {"error": "can't divide by 0."}
    except Exception:
        return {"error": "unknown error."}