from pydantic import BaseModel


class DeliveryHeatMap(BaseModel):
    email: str
    activity: str
    delivered: bool


class DeliveryStudentCount(BaseModel):
    email: str
    count: int


class DeliveryActivityCount(BaseModel):
    activity: str
    count: int
