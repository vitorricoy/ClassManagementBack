from typing import Type, TypeVar
from flask_restful import reqparse
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def parse_from_request(schema: Type[T]):
    parser = reqparse.RequestParser()
    fields = schema.__fields__.keys()
    for field in fields:
        parser.add_argument(field)
    return schema(**parser.parse_args())