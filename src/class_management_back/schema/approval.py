from pydantic import BaseModel


class ApprovalProbability(BaseModel):
    email: str
    probability: float
