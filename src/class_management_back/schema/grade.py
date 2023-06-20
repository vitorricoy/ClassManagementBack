from pydantic import BaseModel

from class_management_back.schema.common import FakeName


class GradeHeatMap(BaseModel):
    email: FakeName
    activity: str
    grade: float


class GradeStudent(BaseModel):
    email: FakeName
    grade: float


class DeliveryActivityCount(BaseModel):
    activity: str
    count: int
