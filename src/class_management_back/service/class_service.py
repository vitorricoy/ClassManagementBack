from class_management_back.model.class_model import ClassModel

class_model = ClassModel()


class ClassService:
    def get_classes(self, user_code: int):
        return class_model.get_classes(user_code)
