from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.routers import rentals, user, bike, admin, auth, stations
from src.app.data.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(bike.router)
app.include_router(rentals.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(stations.router)
