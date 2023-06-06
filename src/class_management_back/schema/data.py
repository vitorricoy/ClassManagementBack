from datetime import datetime
from pydantic import BaseModel, root_validator
from typing import Optional


class DataUploadParams(BaseModel):
    class_name: Optional[str] = None
    class_code: Optional[int] = None
    ignore_user_names: list[str]
    ignore_activities: list[str]

    @root_validator(pre=True)
    def fill_lists(cls, values):
        values["ignore_user_names"] = (
            values.get("ignore_user_names").split(",")
            if values.get("ignore_user_names")
            else []
        )
        values["ignore_activities"] = (
            values.get("ignore_activities").split(",")
            if values.get("ignore_user_names")
            else []
        )
        if not values.get("class_name") and not values.get("class_code"):
            raise ValueError("Need to give class name or code")
        return values


class Class(BaseModel):
    code: int
    name: str
    user_code: int


class Student(BaseModel):
    code: int
    name: str
    email: str
    class_code: int


class Module(BaseModel):
    code: int
    name: str
    class_code: int


class Material(BaseModel):
    code: int
    name: str
    module_code: int


class MaterialView(BaseModel):
    student_code: int
    material_code: int
    hour: datetime


class ClassView(BaseModel):
    student_code: int
    hour: datetime


class ActivityDelivery(BaseModel):
    student_code: int
    material_code: int


class ActivityGrade(BaseModel):
    student_code: int
    material_code: int
    grade: float


class Prediction(BaseModel):
    code: int
    student_code: int
    probability: float
