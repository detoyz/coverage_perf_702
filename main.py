from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
import sqlalchemy as sa

app = FastAPI()

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=True,
)

Base = declarative_base()


class Event(Base):
    __tablename__ = "event"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


@app.get("/hello/{name}")
async def say_hello(name: str):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        for x in range(50):  # assumption is that slowdown caused by each sqlalchemy awaitable, so we want more of them
            await conn.execute(
                sa.insert(Event).values({"name": f"some name {x}"})
            )

    return {"message": f"Hello {name}"}
