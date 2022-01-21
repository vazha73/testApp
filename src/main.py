import sys
import uvicorn
import asyncio
import config
from typing import Optional,List
from loguru import logger
from fastapi import FastAPI
from app.api.routers import router



asyncio.set_event_loop_policy(None)

app = FastAPI()

app.include_router(router)


@app.on_event('startup')
async def startup_event():
    #app.add_event_handler('startup', init_logging)
    logger.info("Server Startup")


@app.on_event('shutdown')
async def shutdown_event():
    # todo close all sessions 
    # todo close all connections
    logger.info("Server Shutdown")

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    if '--reload' in sys.argv:
        uvicorn.run("main:app", host="127.0.0.1", port=config.PORT, log_level="info",reload=True,debug=True)
    else:
        uvicorn.run(app, host=config.HOST, port=config.PORT, log_level="info")
