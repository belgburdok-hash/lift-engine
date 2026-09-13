from pydantic import BaseModel, Field

class LogCreate(BaseModel):
    exercise_name: str = Field(min length=2, max_length=50, description="Название упражнение")
    weight: float = Field(gt=0, description="Рабочий вес в кг")
    reps: int = Field(gt=0, le=30, description="Количество повторений")
    rir: int = Field(default=0, ge=0, le=10, description="Повторения в резерве")


class LogResponse(LogCreate):
    id: int
    estimated_1rm: float    