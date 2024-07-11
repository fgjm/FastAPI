'''
    @author: Giovanni Junco
    @since: 07-06-2024
    @summary: create app
'''
import time
from fastapi import FastAPI, Request
from .routes.orders import router

app = FastAPI(debug=True,
    title="Template FastAPI",
    summary="Application to manage orders in FastAPI and MongoDB.",
)

app.include_router(router)

@app.get("/") 
async def root(): 
    return {
        "Author": "Templates",
        "project": "FastAPI Backend",
        "version": "0.1",
        "contributor": ["Giovanni Junco"]
    }

@app.middleware("http")
async def before_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
