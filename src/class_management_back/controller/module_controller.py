from flask_restful import Resource
from class_management_back.helper.parser import parse_from_request, parse_from_request_with_location

from class_management_back.helper.user import get_user_from_token_with_location
from class_management_back.model.module_model import ModuleModel
from class_management_back.schema.common import ClassCode

module_model = ModuleModel()


class ModuleHeatmapResource(Resource):
    def get(self):
        token_user = get_user_from_token_with_location(location="args")
        class_code = parse_from_request_with_location(
            ClassCode, location="args")
        if not token_user:
            return "Unauthenticated", 401

        module_data = module_model.get_module_heatmap(
            class_code.class_code, token_user.code)

        response = {}

        for entry in module_data:
            if entry.email not in response:
                response[entry.email] = {}
            response[entry.email][entry.module] = entry.conclusion

        return response, 200
