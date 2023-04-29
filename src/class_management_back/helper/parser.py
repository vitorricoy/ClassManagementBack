from typing import Type, TypeVar
from flask_restful import reqparse
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def parse_from_request(schema: Type[T], location=None):
    parser = reqparse.RequestParser()
    fields = schema.__fields__.keys()
    for field in fields:
        parser.add_argument(field, location=location)
    return schema(**parser.parse_args())
