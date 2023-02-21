from flask_restful import Resource, reqparse
import jwt
from class_management_back.environment import JWT_SECRET
from class_management_back.helper.parser import parse_from_request
from class_management_back.helper.user import get_user_from_token
from class_management_back.schema.common import Token
from class_management_back.schema.user import User, UserCreation
from class_management_back.service.user_service import UserService

user_service = UserService()

class UserResource(Resource):
    def post(self):
        args = parse_from_request(UserCreation)
        user = user_service.create_user_by_email_password(args.name, args.email, args.password)
        encoded_jwt = jwt.encode({"code": user.code, "email": user.email, "password": user.password}, JWT_SECRET, algorithm="HS256")
        return encoded_jwt, 200

    def get(self):
        return get_user_from_token(), 200