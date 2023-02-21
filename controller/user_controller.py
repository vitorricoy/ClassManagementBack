from flask_restful import Resource
import jwt
from class_management_back.schema.user import UserCreation
from class_management_back.service.user_service import UserService
user_service = UserService()

class UserResource(Resource):
    def post(self, email, password):
        user = user_service.create_user_by_email_password(email, password)
        encoded_jwt = jwt.encode({"code": user.code, "email": user.email, "password": user.password}, "secret", algorithm="HS256")
        return encoded_jwt, 200

    def get(self, email, password):
        user = user_service.get_user_by_email_password(email, password)
        encoded_jwt = jwt.encode({"code": code, "email": email, "password": password}, "secret", algorithm="HS256")
        return encoded_jwt, 200