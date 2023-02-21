from pydantic import BaseModel


class UserCreation(BaseModel):
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class GetUser(BaseModel):
    email: str
    password: str


class User(BaseModel):
    code: int
    email: str
    name: str
    password: str
