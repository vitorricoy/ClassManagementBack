from flask_restful import Resource
from class_management_back.helper.user import get_user_from_token_with_location

from class_management_back.service.class_service import ClassService

class_service = ClassService()


class ClassResource(Resource):
    def get(self):
        user = get_user_from_token_with_location(location="args")
        if not user:
            return "Unauthenticated", 401
        classes = class_service.get_classes(user.code)
        return [c.dict() for c in classes], 200
