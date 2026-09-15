import aiosqlite
from lift_engine.schemas import LogCreate


class WorkoutRepository:
    def __init__(self, db: aiosqlite.Connection):
        self.db = db

    async def create_log(self, log_data: LogCreate, estimated_1rm: float) -> dict:
        cursor = await self.db.execute(
            """
            INSERT INTO workout_logs (exercise_name, weight, reps, rir, estimated_1rm)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                log_data.exercise_name,
                log_data.weight,
                log_data.reps,
                log_data.rir,
                estimated_1rm,
            ),
        )
        await self.db.commit()

        return {
            "id": cursor.lastrowid,
            "exercise_name": log_data.exercise_name,
            "weight": log_data.weight,
            "reps": log_data.reps,
            "rir": log_data.rir,
            "estimated_1rm": estimated_1rm,
        }

    async def get_all_logs(self) -> list[dict]:
        cursor = await self.db.execute(
            "SELECT id, exercise_name, weight, reps, rir, estimated_1rm FROM workout_logs"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]