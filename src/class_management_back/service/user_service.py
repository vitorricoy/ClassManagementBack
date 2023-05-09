from class_management_back.model.user_model import UserModel
from class_management_back.schema.user import UserCreation, UserLogin

user_model = UserModel()


class UserService:
    def get_user_by_email_password(self, login: UserLogin):
        return user_model.get_by_email_and_password(
            login.email, login.password
        )

    def create_user_by_email_password(self, user: UserCreation):
        return user_model.create(user.name, user.email, user.password)
