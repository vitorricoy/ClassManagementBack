from pydantic import BaseModel


class ProgressMeanStudent(BaseModel):
    email: str
    repetition: float


class ProgressRepetitionMaterialStudent(BaseModel):
    email: str
    material: str
    count: int
    user_mean: float


class ProgressRepetitionMaterial(BaseModel):
    material: str
    count: float
