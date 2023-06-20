from class_management_back.controller.approval_controller import (
    ApprovalProbabilityResource,
)
from class_management_back.controller.class_controller import ClassResource
from class_management_back.controller.delivery_controller import (
    DeliveryActivityCountResource,
    DeliveryHeatmapResource,
    DeliveryStudentCountResource,
)
from class_management_back.controller.frequency_controller import (
    FrequencyHeatmapResource,
    FrequencyStudentMeanResource,
    FrequencyWeekMeanResource,
)
from class_management_back.controller.grade_controller import (
    GradeHeatmapResource,
    GradeStudentResource,
)
from class_management_back.controller.module_controller import (
    ModuleHeatmapResource,
)
from class_management_back.controller.progress_controller import (
    ProgressMeanStudentResource,
    ProgressRepetitionMaterialResource,
    ProgressRepetitionMaterialStudentResource,
)
from class_management_back.controller.user_controller import (
    UserLoginResource,
    UserResource,
)
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

api.add_resource(UserResource, "/user")
api.add_resource(UserLoginResource, "/user/login")
api.add_resource(ClassResource, "/class")
api.add_resource(DeliveryHeatmapResource, "/delivery/heatmap")
api.add_resource(DeliveryStudentCountResource, "/delivery/student_count")
api.add_resource(DeliveryActivityCountResource, "/delivery/activity_count")
api.add_resource(GradeHeatmapResource, "/grade/heatmap")
api.add_resource(GradeStudentResource, "/grade/student")
api.add_resource(ModuleHeatmapResource, "/module/heatmap")
api.add_resource(ProgressMeanStudentResource, "/progress/mean_student")
api.add_resource(
    ProgressRepetitionMaterialStudentResource,
    "/progress/repetition_material_student",
)
api.add_resource(
    ProgressRepetitionMaterialResource, "/progress/repetition_material"
)
api.add_resource(FrequencyHeatmapResource, "/frequency/heatmap")
api.add_resource(FrequencyStudentMeanResource, "/frequency/student_mean")
api.add_resource(FrequencyWeekMeanResource, "/frequency/week_mean")
api.add_resource(ApprovalProbabilityResource, "/approval/probability")

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def index():
    return "Index Page"


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
