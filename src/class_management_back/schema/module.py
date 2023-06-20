from pydantic import BaseModel

from class_management_back.schema.common import FakeName


class ModuleHeatMap(BaseModel):
    email: FakeName
    module: str
    conclusion: float
