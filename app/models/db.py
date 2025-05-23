from typing_extensions import Literal
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.models.generation import Base, GenerationTask


engine = create_async_engine("sqlite+aiosqlite:///./pixverse.db")
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


async def save_generation_task(
    session: AsyncSession,
    request_type: Literal["text", "img"],
    app_bundle_id: str,
    apphud_user_id: str,
    prompt: str,
):
    task = GenerationTask(
        request_type=request_type,
        app_bundle_id=app_bundle_id,
        apphud_user_id=apphud_user_id,
        prompt=prompt,
    )
    session.add(task)
    await session.commit()
