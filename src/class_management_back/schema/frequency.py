from pydantic import BaseModel


class FrequencyHeatMap(BaseModel):
    email: str
    week: str
    frequency: int


class FrequencyStudentMean(BaseModel):
    email: str
    frequency: float


class FrequencyWeekMean(BaseModel):
    week: str
    frequency: float
