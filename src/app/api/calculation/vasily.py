from enum import Enum

from fastapi import APIRouter, Response
from pydantic import BaseModel, Field, validator

router = APIRouter()


class Operations(str, Enum):
    add = "+"
    sub = '-'
    mul = '*'
    div = '/'


class CalcRequest(BaseModel):
    x: float = Field(description="float", ge=-10 ** 32, le=10 ** 32, example=5)
    y: float = Field(description="float", ge=-10 ** 32, le=10 ** 32, example=2)
    operation: Operations = Field(description="add, multiply, subtract or divide", example=Operations.add)

    @validator("operation")
    def validate_all_fields_one_by_one(cls, field_value, values):
        if field_value == Operations.div and values["y"] == 0:
            raise ValueError("Division by zero isn't allowed")
        return field_value


class Result(BaseModel):
    success: bool
    message: str = None
    result: float = None


class CalcResult(BaseModel):
    result: float
    operation: str


def calculate(x: float, y: float, oper: Operations) -> CalcResult:
    match oper:
        case Operations.add:
            return CalcResult(result=x + y, operation="+")
        case Operations.sub:
            return CalcResult(result=x - y, operation="-")
        case Operations.mul:
            return CalcResult(result=x * y, operation="*")
        case Operations.div:
            return CalcResult(result=x / y, operation="/")
        case _:
            raise Exception(f'invalid parameter value "op = {oper}")')


@router.post("/vasily/calculator", name="calculator by Vasia", response_model=Result)
async def read_root(request: CalcRequest, response: Response) -> Result:
    res = calculate(x=request.x, y=request.y, oper=request.operation)
    return Result(success=True, result=res.result, message=f"{request.x} {res.operation} {request.y} = {res.result}")
