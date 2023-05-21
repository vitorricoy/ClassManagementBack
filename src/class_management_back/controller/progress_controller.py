from flask_restful import Resource
from class_management_back.helper.parser import parse_from_request_with_location

from class_management_back.helper.user import get_user_from_token_with_location
from class_management_back.model.progress_model import ProgressModel
from class_management_back.schema.common import ClassCode

progress_model = ProgressModel()


class ProgressMeanStudentResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args")
        if not token_user:
            return "Unauthenticated", 401

        progress_data = progress_model.get_mean_student(
            class_code.class_code, token_user.code)

        return [p.dict() for p in progress_data], 200


class ProgressRepetitionMaterialStudentResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args")
        if not token_user:
            return "Unauthenticated", 401

        progress_data = progress_model.get_repetition_material_student(
            class_code.class_code, token_user.code)

        return [p.dict() for p in progress_data], 200


class ProgressRepetitionMaterialResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args")
        if not token_user:
            return "Unauthenticated", 401

        progress_data = progress_model.get_repetition_material(
            class_code.class_code, token_user.code)

        return [p.dict() for p in progress_data], 200
