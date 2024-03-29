from flask_restful import Resource
from class_management_back.helper.parser import (
    parse_from_request,
    parse_from_request_with_location,
)

from class_management_back.helper.user import (
    get_user_from_token,
    get_user_from_token_with_location,
)
from class_management_back.model.delivery_model import DeliveryModel
from class_management_back.schema.common import ClassCode

delivery_model = DeliveryModel()


class DeliveryHeatmapResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args"
        )
        if not token_user:
            return "Unauthenticated", 401

        delivery_data = delivery_model.get_delivery_heatmap(
            class_code.class_code, token_user.code
        )

        response = {}

        for entry in delivery_data:
            if entry.email not in response:
                response[entry.email] = {}
            response[entry.email][entry.activity] = entry.delivered

        return response, 200


class DeliveryStudentCountResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args"
        )
        if not token_user:
            return "Unauthenticated", 401

        delivery_data = delivery_model.get_delivery_student_count(
            class_code.class_code, token_user.code
        )

        return [d.dict() for d in delivery_data], 200


class DeliveryActivityCountResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args"
        )
        if not token_user:
            return "Unauthenticated", 401

        delivery_data = delivery_model.get_delivery_activity_count(
            class_code.class_code, token_user.code
        )

        return [d.dict() for d in delivery_data], 200
