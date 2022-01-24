from fastapi import APIRouter
from pydantic import BaseModel, validator, Field
from enum import Enum
router = APIRouter()


class Operations(str, Enum):
    plus = 'plus'
    minus = 'minus'
    multiply = 'multiply'
    divide = 'divide'
    
class Result(BaseModel):
    asnwer: float
    
class Calculator(BaseModel):
    a: float = Field(description="Float", ge=-10**32, le=10**32, example=3.5)
    b: float = Field(description="Float", ge=-10**32, le=10**32, example=1.5)
    op: str = Field(description="plus, minus, multiply, divide", example="plus")

    @validator("op")
    def is_valid_operator(cls, op, values):
        operators = ("plus", "minus", "multiply", "divide")
        if op not in operators:
            raise ValueError("invalid operator. must be (plus, minus, multiply, divide)")
        elif values["b"] == 0 and op == "divide":
            raise ValueError("can't divide by 0")
        return op     

    def ___init___(self, a, b, op):
        self.a = a
        self.b = b
        self.op = op

    def solution(self):
        if self.op == Operations.plus:
            return self.a + self.b
        elif self.op == Operations.minus:
            return self.a - self.b
        elif self.op == Operations.multiply:
            return self.a * self.b
        elif self.op == Operations.divide:
            return self.a / self.b


@router.post("/giorgi/calculator/",response_model=Result,)
async def read_root(calculator: Calculator):
    """Calculator"""
    return Result(answer=calculator.solution())

    


# @router.post("/giorgi/calculator/")
# async def read_root(a: int, b: int, op:str):
#     # using anonymous functions to define operators
#     operators = {"plus": (lambda a,b: a+b), "minus": (lambda a,b: a-b), "multiply": (lambda a,b: a*b), "divide": (lambda a,b: a/b)}
#     if op not in operators.keys():
#         return {"error": "operator unknown. use (plus, minus, multiply, divide)"}

#     try:
#         return operators[op] (a, b)
#     except ZerodivideError:
#         return {"error": "can't divide by 0"}
#     except Exception:
#         return {"error": "unknown error"}