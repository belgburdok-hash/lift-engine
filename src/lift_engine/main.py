from contextlib import asynccontextmanager

from fastapi import FastAPI

from lift_engine.database import init_db
from lift_engine.router import router as workout_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код до yield выполняется при запуске приложения
    await init_db()
    yield
    # Код после yield выполняется при выключении приложения


app = FastAPI(
    title="Lift Engine API",
    description="Асинхронный сервис расчета 1RM и учета тренировочных подходов",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(workout_router)


@app.get("/")
async def root():
    return {"message": "Lift Engine is running", "status": "ok"}