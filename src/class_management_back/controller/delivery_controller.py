from flask_restful import Resource

from class_management_back.helper.user import get_user_from_token


class UserLoginResource(Resource):
    def get(self):
        token_user = get_user_from_token()
        if not token_user:
            return "Unauthenticated", 401
