from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.db import init_db, engine
from app.routers.pixverse import router as pixverse_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(title="Pixverse Integration API", version="1.0.0", lifespan=lifespan)

app.include_router(pixverse_router)
