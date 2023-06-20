from pydantic import BaseModel

from class_management_back.schema.common import FakeName


class DeliveryHeatMap(BaseModel):
    email: FakeName
    activity: str
    delivered: bool


class DeliveryStudentCount(BaseModel):
    email: FakeName
    count: int


class DeliveryActivityCount(BaseModel):
    activity: str
    count: int
