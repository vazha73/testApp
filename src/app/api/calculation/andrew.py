from fastapi import APIRouter, Response, status
from pydantic import BaseModel, Field
from enum import Enum


router = APIRouter()


class Operation(str, Enum):
    add = "add"
    multiply = "multiply"
    subtract = "subtract"
    divide = "divide"


class CalcRequest(BaseModel):
    a: float = Field(description="float", ge=-10 ** 32, le=10 ** 32, example=5)
    b: float = Field(description="float", ge=-10 ** 32, le=10 ** 32, example=3)
    operation: Operation = Field(description="add, multiply, subtract or divide", example=Operation.add)

    @classmethod
    def validate_all_fields_one_by_one(cls, field_value, values):
        if field_value == Operation.divide and values["x2"] == 0:
            raise ValueError('Division by zero is not allowed')
        return field_value

    class Config:
        use_enum_values = True


class Result(BaseModel):
    success: bool
    message: str = None
    result: float = None


class CalcResult(BaseModel):
    result: float
    operation: str


def calculate(a: float, b: float, op: Operation) -> CalcResult:
    match op:
        case Operation.add:
            return CalcResult(result=a + b, operation="+")
        case Operation.subtract:
            return CalcResult(result=a - b, operation="-")
        case Operation.multiply:
            return CalcResult(result=a * b, operation="*")
        case Operation.divide:
            return CalcResult(result=a / b, operation="/")
        case _:
            raise Exception(f'invalid parameter value "op = {op}")')


@router.post("/andrew/calculator",
             name="calc by Andrew",
             response_model=Result,
             status_code=status.HTTP_200_OK)
async def read_root(request: CalcRequest, response: Response) -> Result:
    res = calculate(a=request.a, b=request.b, op=request.operation)
    return Result(success=True, result=res.result, message=f"{request.a} {res.operation} {request.b} = {res.result}")
