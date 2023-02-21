from flask_restful import Resource, reqparse
import jwt
from class_management_back.environment import JWT_SECRET
from class_management_back.exceptions.user import (
    AccountAlreadyExistsException,
    CouldNotFoundAccountException,
    ErrorCreatingAccountException,
)
from class_management_back.helper.parser import parse_from_request
from class_management_back.helper.user import get_user_from_token
from class_management_back.schema.common import Token
from class_management_back.schema.user import User, UserCreation, UserLogin
from class_management_back.service.user_service import UserService

user_service = UserService()


class UserResource(Resource):
    def post(self):
        try:
            args = parse_from_request(UserCreation)
            user = user_service.create_user_by_email_password(args)
            return (
                jwt.encode({**user.dict()}, JWT_SECRET, algorithm="HS256"),
                200,
            )
        except AccountAlreadyExistsException:
            return "AccountAlreadyExists", 400
        except ErrorCreatingAccountException:
            return "ErrorCreatingAccount", 400

    def get(self):
        try:
            token_user = get_user_from_token()
            if token_user:
                return token_user, 200
            args = parse_from_request(UserLogin)
            user = user_service.get_user_by_email_password(args)
            return (
                jwt.encode({**user.dict()}, JWT_SECRET, algorithm="HS256"),
                200,
            )
        except CouldNotFoundAccountException:
            return "CouldNotFoundAccount", 400
