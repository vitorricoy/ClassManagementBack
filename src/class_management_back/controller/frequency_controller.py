from flask_restful import Resource
from class_management_back.helper.parser import (
    parse_from_request_with_location,
)

from class_management_back.helper.user import get_user_from_token_with_location
from class_management_back.model.frequency_model import FrequencyModel
from class_management_back.schema.common import ClassCode

frequency_model = FrequencyModel()


class FrequencyHeatmapResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args"
        )
        if not token_user:
            return "Unauthenticated", 401

        frequency_data = frequency_model.get_heatmap(
            class_code.class_code, token_user.code
        )

        response = {}

        for entry in frequency_data:
            if entry.email not in response:
                response[entry.email] = {}
            response[entry.email][entry.week] = entry.frequency

        return response, 200


class FrequencyStudentMeanResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args"
        )
        if not token_user:
            return "Unauthenticated", 401

        frequency_data = frequency_model.get_student_mean(
            class_code.class_code, token_user.code
        )

        return [f.dict() for f in frequency_data], 200


class FrequencyWeekMeanResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args"
        )
        if not token_user:
            return "Unauthenticated", 401

        frequency_data = frequency_model.get_week_mean(
            class_code.class_code, token_user.code
        )

        return [f.dict() for f in frequency_data], 200
