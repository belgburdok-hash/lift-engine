import aiosqlite
from fastapi import APIRouter, Depends, status

from lift_engine.database import get_db
from lift_engine.repository import WorkoutRepository
from lift_engine.schemas import LogCreate, LogResponse
from lift_engine.services import calculate_e1rm

router = APIRouter(prefix="/logs", tags=["Workout Logs"])


@router.post("", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def create_workout_log(
    payload: LogCreate,
    db: aiosqlite.Connection = Depends(get_db),
):
    """Принимает подход, считает расчетный 1ПМ и сохраняет запись в базу данных."""
    result = calculate_e1rm(weight=payload.weight, reps=payload.reps, rir=payload.rir)
    e1rm = result["average"]

    repo = WorkoutRepository(db)
    new_log = await repo.create_log(log_data=payload, estimated_1rm=e1rm)
    return new_log


@router.get("", response_model=list[LogResponse])
async def get_workout_logs(
    db: aiosqlite.Connection = Depends(get_db),
):
    """Возвращает историю всех сохраненных подходов."""
    repo = WorkoutRepository(db)
    return await repo.get_all_logs()