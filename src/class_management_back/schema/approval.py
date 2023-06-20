from pydantic import BaseModel
from class_management_back.schema.common import FakeName


class ApprovalProbability(BaseModel):
    email: FakeName
    probability: float
