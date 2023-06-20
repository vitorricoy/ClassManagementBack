from faker import Faker
from pydantic import BaseModel


class Token(BaseModel):
    token: str


class ClassCode(BaseModel):
    class_code: int


faker = Faker()
fake_name_map = {

}


class FakeName(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v:
            if v not in fake_name_map:
                faker.seed_instance(v)
                fake_name_map[v] = faker.name()
            return fake_name_map.get(v)
        return v
