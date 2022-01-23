from fastapi import APIRouter
from pydantic import BaseModel, validator, ValidationError
router = APIRouter()

class Calculator(BaseModel):
    a: float
    b: float
    op: str

    @validator("op")
    def is_valid_operator(cls, op, values):
        operators = ("plus", "minus", "multiply", "divide")
        if op not in operators:
            raise ValueError("invalid operator. must be (plus, minus, multiply, divide)")
        elif values["b"] == 0 and op == "divide":
            raise ValueError("can't divide by 0")
        return op        

class Calculate:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def solution(self, op):
        if op == "plus":
            return self.a + self.b
        elif op == "minus":
            return self.a - self.b
        elif op == "multiply":
            return self.a * self.b
        elif op == "divide":
            return self.a / self.b

@router.post("/giorgi/calculator/")
async def read_root(calculator: Calculator):
    answer = Calculate(calculator.a, calculator.b)
    return answer.solution(calculator.op)


# @router.post("/giorgi/calculator/")
# async def read_root(a: int, b: int, op:str):
#     # using anonymous functions to define operators
#     operators = {"plus": (lambda a,b: a+b), "minus": (lambda a,b: a-b), "multiply": (lambda a,b: a*b), "divide": (lambda a,b: a/b)}
#     if op not in operators.keys():
#         return {"error": "operator unknown. use (plus, minus, multiply, divide)"}

#     try:
#         return operators[op] (a, b)
#     except ZeroDivisionError:
#         return {"error": "can't divide by 0"}
#     except Exception:
#         return {"error": "unknown error"}