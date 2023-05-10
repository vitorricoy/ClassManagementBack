from class_management_back.controller.class_controller import ClassResource
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

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def index():
    return "Index Page"


if __name__ == "__main__":
    app.run(debug=True, port=8787, host="0.0.0.0")
