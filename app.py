from class_management_back.controller.user_controller import UserResource
from class_management_back.controller.data_controller import DataResource
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)

api.add_resource(DataResource, "/data")
api.add_resource(UserResource, "/user")
load_dotenv()

if __name__ == "__main__":
    app.run(debug=True)
