from pydantic import BaseModel

from class_management_back.schema.common import FakeName


class ProgressMeanStudent(BaseModel):
    email: FakeName
    repetition: float


class ProgressRepetitionMaterialStudent(BaseModel):
    email: FakeName
    material: str
    count: int
    user_mean: float


class ProgressRepetitionMaterial(BaseModel):
    material: str
    count: float
