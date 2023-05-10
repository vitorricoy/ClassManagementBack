from pydantic import BaseModel


class DeliveryHeatMap(BaseModel):
    email: str
    activity: str
    delivered: bool
