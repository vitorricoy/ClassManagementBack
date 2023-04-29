from class_management_back.controller.user_controller import UserResource
from class_management_back.controller.data_controller import DataResource
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(DataResource, "/data")
api.add_resource(UserResource, "/user")


@app.route("/")
def index():
    return "Index Page"


if __name__ == "__main__":
    app.run(debug=True, port=8787, host="0.0.0.0")
