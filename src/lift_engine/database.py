import aiosqlite

DB_NAME="lift_engine.db"

async def init_db():
    "Создает таблицу подходов при первом запуске приложения"
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute ("""
            CREATE TABLE IF NOT EXISTS workout_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_name TEXT NOT NULL,
                weight REAL NOT NULL,
                reps INTEGER NOT NULL,
                rir INTEGER NOT NULL,
                estimated_1rm REAL NOT NULL
            )
        """)
        await db.commit()
async def get_db():
    """Генератор асинхронной сессии для FastAPI (Dependency Injection)."""
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        yield db