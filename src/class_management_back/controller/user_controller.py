import hashlib
from flask_restful import Resource
import jwt
from class_management_back.environment import JWT_SECRET
from class_management_back.exceptions.user import (
    AccountAlreadyExistsException,
    CouldNotFindAccountException,
    ErrorCreatingAccountException,
)
from class_management_back.helper.parser import parse_from_request
from class_management_back.helper.user import get_user_from_token
from class_management_back.schema.user import UserCreation, UserLogin
from class_management_back.service.user_service import UserService

user_service = UserService()


class UserResource(Resource):
    def post(self):
        try:
            args = parse_from_request(UserCreation)
            hash = hashlib.sha256()
            hash.update(args.password.encode("utf8"))
            args.password = hash.hexdigest()
            user = user_service.create_user_by_email_password(args)
            user_dict = user.dict()
            del user_dict["password"]
            return (
                jwt.encode({**user_dict}, JWT_SECRET, algorithm="HS256"),
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
            hash = hashlib.sha256()
            hash.update(args.password.encode("utf8"))
            args.password = hash.hexdigest()
            user = user_service.get_user_by_email_password(args)
            return (
                jwt.encode({**user.dict()}, JWT_SECRET, algorithm="HS256"),
                200,
            )
        except CouldNotFindAccountException:
            return "CouldNotFindAccount", 400
