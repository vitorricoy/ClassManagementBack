from pydantic import BaseModel


class DataUploadParams(BaseModel):
    ignore_user_names: list[str]
