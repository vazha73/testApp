import json
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from  app.api.calculation.vazha import Result,calculate
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY,HTTP_200_OK


class TestCalculatorRoutes:
   @pytest.mark.asyncio
   async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("vazha:calculator"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

   @pytest.mark.asyncio
   @pytest.mark.parametrize(
        "params, result, status_code",
        (
            ({"x1": 2,"x2": 2, "operation": "add"},4, HTTP_200_OK),
            ({"x1": 2,"x2": 2, "operation": "subtract"},0, HTTP_200_OK),
            ({"x1": 2,"x2": 2, "operation": "multiply"},4, HTTP_200_OK),
            ({"x1": 543,"x2": 22.331, "operation": "divide"},24.315973310644395, HTTP_200_OK),
            ({"x1": 2,"x2": 0, "operation": "divide"},1, HTTP_422_UNPROCESSABLE_ENTITY),
        )
   )
   async def test_route(self, app: FastAPI, client: AsyncClient,params: dict,result:float,status_code: int) -> None:
        res = await client.post(app.url_path_for("vazha:calculator"), json=params)
        assert res.status_code == status_code
        if status_code==HTTP_200_OK:
           data=Result(**res.json())
           assert data.success == True
           assert data.result == result
        
        
        
class TestCalculator:
   @pytest.mark.parametrize(
        "params, result",
        (
            ({"x1": 2.33,"x2": 55.112, "op": "add"},57.442),
            ({"x1": 2,"x2": 2, "op": "subtract"},0),
            ({"x1": 2,"x2": 2, "op": "multiply"},4),
            ({"x1": 2,"x2": 2, "op": "divide"},1)
        )
   )
   def testCalcFunction(self, params: dict,result: float)->None:
      data = calculate(**params)
      assert data.result == result
