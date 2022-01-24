from fastapi import APIRouter, Response, status
from pydantic import BaseModel, Field
from enum import Enum

import pydantic

router = APIRouter()


class Operation(str, Enum):
    add = "add"
    multiply = "multiply"
    subtract = "subtract"
    divide = "divide"


class CalcRequest(BaseModel):
    x1: float = Field(description="float", ge=-10**32, le=10**32,example=3.5)
    x2: float = Field(description="float", ge=-10**32, le=10**32,example=1.5)
    operation: Operation = Field(
        description="add, multiply, subtract or divide",example=Operation.add)

    @pydantic.validator("operation")
    @classmethod
    def validate_all_fields_one_by_one(cls, field_value, values):
        if field_value == Operation.divide and values["x2"] == 0:
            raise ValueError('Division by zero is not allowed')
        return field_value

    class Config:
        use_enum_values = True


class Result (BaseModel):
    success: bool
    message: str = None
    result: float = None


class CalcResult(BaseModel):
    result: float
    operation: str


def calculate(x1: float, x2: float, op: Operation) -> CalcResult:
    match op:
        case Operation.add:
            return CalcResult(result=x1+x2, operation="+")
        case Operation.subtract:
            return CalcResult(result=x1-x2, operation="-")
        case Operation.multiply:
            return CalcResult(result=x1*x2, operation="*")
        case Operation.divide:
            return CalcResult(result=x1/x2, operation="/")
        case _:
            raise Exception(f'invalid parameter value "op = {op}")')


@router.post("/vazha/calculator",
             name="vazha:calculator",
             response_model=Result,
             status_code=status.HTTP_200_OK)
async def read_root(request: CalcRequest, response: Response) -> Result:
    """
    # The best and fast calculator.

    💡 The calculator can add, subtract, multiply and divide.

    ### ⚠️ Warning: Division by zero is not allowed

    --------------------------------------------------------
    Author : Vazha Meladze :)
    """
    res = calculate(x1=request.x1, x2=request.x2, op=request.operation)
    return Result(success=True, result=res.result, message=f"{request.x1} {res.operation} {request.x2} = {res.result}")
    #return {"success": True, "result": res.result, "message": f"{request.x1} {res.operation} {request.x2} = {res.result}"}
