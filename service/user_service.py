from class_management_back.schema.user import User


class UserService:
    def get_user_by_email_password(self, email: str, password: str):
        return User(code=1, name='teste', email='teste', password='teste')
        
    def create_user_by_email_password(self, name: str, email: str, password: str):
        return User(code=1, name='teste', email='teste', password='teste')