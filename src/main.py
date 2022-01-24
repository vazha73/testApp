import sys
import uvicorn
import asyncio
import config
from typing import Optional,List
from loguru import logger
from fastapi import FastAPI
from app.api.routers import router
from app.api.calculation.andrew import router as andrew_router
from app.api.calculation.george import router as george_router
from app.api.calculation.vasily import router as vasily_router
from app.api.calculation.vazha import router as vazha_router

asyncio.set_event_loop_policy(None)

tags_metadata = [
    {
        "name": "Test",
        "description": "Operations with Dashboard. ",
    },
    {
        "name": "Obsrvation",
        "description": "Operations with chat.",
    },
    {
        "name": "default",
        "description": "todo remove this tag",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
app = FastAPI(
    title="Text Service Massage Fabric",
    debug=True,
    openapi_tags=tags_metadata
    )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=env_origins.split(sep=','),
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
app.include_router(router)
app.include_router(andrew_router)
app.include_router(george_router)
app.include_router(vasily_router)
app.include_router(vazha_router)

def get_application():
     return app

@app.on_event('startup')
async def startup_event():
    #app.add_event_handler('startup', init_logging)
    logger.info("Server Startup")
    print(f"Server Startup http://localhost:{config.PORT}")
    print (f"swagger docs: http://localhost:{config.PORT}/docs")


@app.on_event('shutdown')
async def shutdown_event():
    # todo close all sessions 
    # todo close all connections
    logger.info("Server Shutdown")

 
if __name__ == '__main__':
    if '--reload' in sys.argv:
        uvicorn.run("main:app", host="127.0.0.1", port=config.PORT, log_level="info",reload=True,debug=True)
    else:
        uvicorn.run(app, host=config.HOST, port=config.PORT, log_level="info")
