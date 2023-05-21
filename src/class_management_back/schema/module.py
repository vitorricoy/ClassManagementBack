from pydantic import BaseModel


class ModuleHeatMap(BaseModel):
    email: str
    module: str
    conclusion: float
