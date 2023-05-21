from io import StringIO
from flask import request
from flask_restful import Resource
import pandas as pd
from class_management_back.helper.parser import (
    parse_from_request_with_location,
)
from class_management_back.helper.user import get_user_from_token_with_location
from class_management_back.schema.data import DataUploadParams

from class_management_back.service.class_service import ClassService
from class_management_back.service.data_service import DataService

class_service = ClassService()
data_service = DataService()


class ClassResource(Resource):
    def get(self):
        user = get_user_from_token_with_location(location="args")
        if not user:
            return "Unauthenticated", 401
        classes = class_service.get_classes(user.code)
        return [c.dict() for c in classes], 200

    def post(self):
        file_log = request.files.get("file_log")
        file_delivery = request.files.get("file_delivery")
        file_grade = request.files.get("file_grade")
        if not file_log or not file_delivery or not file_grade:
            return "InvalidFile", 400
        log_data = pd.read_csv(
            StringIO(file_log.read().decode("utf-8")), encoding="utf-8"
        )
        delivery_data = pd.read_csv(
            StringIO(file_delivery.read().decode("utf-8")), encoding="utf-8"
        )
        grade_data = pd.read_csv(
            StringIO(file_grade.read().decode("utf-8")), encoding="utf-8"
        )
        args = parse_from_request_with_location(DataUploadParams, "form")
        new_class = data_service.process_data(
            log_data, delivery_data, grade_data, args
        )

        user = get_user_from_token_with_location(location="form")
        if not user:
            return "Unauthenticated", 401

        return new_class.dict(), 200
