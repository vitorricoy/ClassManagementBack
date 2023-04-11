from datetime import datetime
from pydantic import BaseModel


class DataUploadParams(BaseModel):
    class_name: str
    ignore_user_names: list[str]
    ignore_activities: list[str]


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
