from pydantic import BaseModel


class Token(BaseModel):
    token: str


class ClassCode(BaseModel):
    class_code: int
