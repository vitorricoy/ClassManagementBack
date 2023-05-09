import jwt
from class_management_back.environment import JWT_SECRET
from class_management_back.helper.parser import (
    parse_from_request,
    parse_from_request_with_location,
)
from class_management_back.schema.common import Token
from class_management_back.schema.user import User


def get_user_from_token():
    try:
        args = parse_from_request(Token)
    except:
        return None
    return User(**jwt.decode(args.token, JWT_SECRET, algorithms=["HS256"]))


def get_user_from_token_with_location(location: str):
    try:
        args = parse_from_request_with_location(Token, location=location)
    except:
        return None
    return User(**jwt.decode(args.token, JWT_SECRET, algorithms=["HS256"]))
