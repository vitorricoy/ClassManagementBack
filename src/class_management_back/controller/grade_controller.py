from flask_restful import Resource
from class_management_back.helper.parser import (
    parse_from_request,
    parse_from_request_with_location,
)

from class_management_back.helper.user import (
    get_user_from_token,
    get_user_from_token_with_location,
)
from class_management_back.model.grade_model import GradeModel
from class_management_back.schema.common import ClassCode

grade_model = GradeModel()


class GradeHeatmapResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args"
        )
        if not token_user:
            return "Unauthenticated", 401

        grade_data = grade_model.get_grade_heatmap(
            class_code.class_code, token_user.code
        )

        response = {}

        for entry in grade_data:
            if entry.email not in response:
                response[entry.email] = {}
            response[entry.email][entry.activity] = entry.grade

        return response, 200


class GradeStudentResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args"
        )
        if not token_user:
            return "Unauthenticated", 401

        grade_data = grade_model.get_grade_student(
            class_code.class_code, token_user.code
        )

        return [g.dict() for g in grade_data], 200
