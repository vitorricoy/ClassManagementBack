from pydantic import BaseModel


class GradeHeatMap(BaseModel):
    email: str
    activity: str
    grade: float


class GradeStudent(BaseModel):
    email: str
    grade: float


class DeliveryActivityCount(BaseModel):
    activity: str
    count: int
