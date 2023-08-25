from fastapi import FastAPI, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import create_database
from api.routes.record import record
from redis_cache.redis_conn import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


import uvicorn

app = FastAPI(title="gooddelo_test_case")

@app.on_event("startup")
async def startup():
    FastAPICache.init(RedisBackend(redis), prefix="fastapi_cache")
    routes = [record.router]
    for route in routes:
        app.include_router(route)
    await create_database()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)