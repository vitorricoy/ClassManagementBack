import jwt
from class_management_back.environment import JWT_SECRET
from class_management_back.helper.parser import parse_from_request
from class_management_back.schema.common import Token
from class_management_back.schema.user import User


def get_user_from_token(location=None):
    args = parse_from_request(Token, location=location)
    return User(**jwt.decode(args.token, JWT_SECRET, algorithms=["HS256"]))
