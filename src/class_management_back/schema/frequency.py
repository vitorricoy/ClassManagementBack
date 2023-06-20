from pydantic import BaseModel

from class_management_back.schema.common import FakeName


class FrequencyHeatMap(BaseModel):
    email: FakeName
    week: str
    frequency: int


class FrequencyStudentMean(BaseModel):
    email: FakeName
    frequency: float


class FrequencyWeekMean(BaseModel):
    week: str
    frequency: float
