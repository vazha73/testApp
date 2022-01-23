from fastapi import APIRouter, Response, status
from pydantic import BaseModel, Field
from enum import Enum
from decimal import Decimal

router = APIRouter()


class Operation(str, Enum):
    add = "add"
    multiply = "multiply"
    subtract = "subtract"
    divide = "divide"


class CalcRequest(BaseModel):
    x1: Decimal = Field(description="Decimal", ge=-10**64, le=10**64)
    x2: Decimal = Field(description="Decimal", ge=-10**64, le=10**64)
    operation: Operation = Field(
        description="add, multiply, subtract or divide")

    class Config:
        use_enum_values = True


class Result (BaseModel):
    success: bool
    message: str = None
    result: Decimal = None


class CalcResult(BaseModel):
    result: Decimal
    operation: str


def calculate(x1: Decimal, x2: Decimal, op: Operation) -> CalcResult:
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
            raise Exception('I know Python!')


@router.post("/vazha_calc",
             name="vazha_calc",
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
    if request.operation == Operation.divide and request.x2 == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        #raise HTTPException(status_code=422, detail="Cannot divide by zero. Division by zero is not allowed")
        return {"success": False, "message": "Cannot divide by zero. Division by zero is not allowed"}

    res = calculate(x1=request.x1, x2=request.x2, op=request.operation)
    return {"success": True, "result": res.result, "message": f"{request.x1} {res.operation} {request.x2} = {res.result}"}
