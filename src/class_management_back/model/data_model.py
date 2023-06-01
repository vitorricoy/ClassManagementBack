from class_management_back.db.config import query_db
from class_management_back.exceptions.log_data import (
    ErrorCreatingActivityDeliveryException,
    ErrorCreatingActivityGradeException,
    ErrorCreatingClassException,
    ErrorCreatingClassViewException,
    ErrorCreatingMaterialException,
    ErrorCreatingMaterialViewException,
    ErrorCreatingModuleException,
    ErrorCreatingPredictionException,
    ErrorCreatingStudentException,
)
from class_management_back.schema.data import (
    ActivityDelivery,
    ActivityGrade,
    Class,
    ClassView,
    Material,
    MaterialView,
    Module,
    Prediction,
    Student,
)


class DataModel:
    def create_class(self, name: str, user_code: int):
        query = """
            INSERT INTO 
                class (
                    name, 
                    user_code
                ) 
            VALUES(
                :name, 
                :user_code
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(query, name=name, user_code=user_code)
        if not result or not result[0]:
            raise ErrorCreatingClassException()
        return Class(**result[0])

    def create_student(self, name: str, email: str, class_code: int):
        query = """
            INSERT INTO 
                student (
                    name, 
                    email,
                    class_code
                ) 
            VALUES(
                :name, 
                :email,
                :class_code
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(query, name=name, class_code=class_code, email=email)
        if not result or not result[0]:
            raise ErrorCreatingStudentException()
        return Student(**result[0])

    def create_module(self, name: str, class_code: int):
        query = """
            INSERT INTO 
                module (
                    name,
                    class_code
                ) 
            VALUES(
                :name, 
                :class_code
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(query, name=name, class_code=class_code)
        if not result or not result[0]:
            raise ErrorCreatingModuleException()
        return Module(**result[0])

    def create_material(self, name: str, module_code: int):
        query = """
            INSERT INTO 
                material (
                    name,
                    module_code
                ) 
            VALUES(
                :name, 
                :module_code
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(query, name=name, module_code=module_code)
        if not result or not result[0]:
            raise ErrorCreatingMaterialException()
        return Material(**result[0])

    def create_class_view(self, student_code: int, hour: str):
        query = """
            INSERT INTO 
                class_view (
                    student_code,
                    hour
                ) 
            VALUES(
                :student_code, 
                :hour
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(query, student_code=student_code, hour=hour)
        if not result or not result[0]:
            raise ErrorCreatingClassViewException()
        return ClassView(**result[0])

    def create_material_view(
        self, material_code: int, student_code: int, hour: str
    ):
        query = """
            INSERT INTO 
                material_view (
                    student_code,
                    material_code,
                    hour
                ) 
            VALUES(
                :student_code, 
                :material_code,
                :hour
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(
            query,
            student_code=student_code,
            material_code=material_code,
            hour=hour,
        )
        if not result or not result[0]:
            raise ErrorCreatingMaterialViewException()
        return MaterialView(**result[0])

    def create_activity_delivery(self, material_code: int, student_code: int):
        query = """
            INSERT INTO 
                activity_delivery (
                    student_code,
                    material_code
                ) 
            VALUES(
                :student_code, 
                :material_code
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(
            query, student_code=student_code, material_code=material_code
        )
        if not result or not result[0]:
            raise ErrorCreatingActivityDeliveryException()
        return ActivityDelivery(**result[0])

    def create_activity_grade(
        self, material_code: int, student_code: int, grade: float
    ):
        query = """
            INSERT INTO 
                activity_grade (
                    student_code,
                    material_code,
                    grade
                ) 
            VALUES(
                :student_code, 
                :material_code,
                :grade
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(
            query,
            student_code=student_code,
            material_code=material_code,
            grade=grade,
        )
        if not result or not result[0]:
            raise ErrorCreatingActivityGradeException()
        return ActivityGrade(**result[0])

    def create_approval_prediction(
        self, student_code: int, probability: float
    ):
        query = """
            INSERT INTO 
                approval_prediction (
                    student_code,
                    probability
                ) 
            VALUES(
                :student_code, 
                :probability
            )
            ON CONFLICT DO NOTHING
            RETURNING *;
        """
        result = query_db(
            query,
            student_code=student_code,
            probability=probability,
        )
        if not result or not result[0]:
            raise ErrorCreatingPredictionException()
        return Prediction(**result[0])

    def delete_class(self, class_code: int):
        query = """
            DELETE FROM class_view WHERE student_code IN (SELECT code FROM student WHERE class_code = :class_code);

            DELETE FROM material_view WHERE student_code IN (SELECT code FROM student WHERE class_code = :class_code);

            DELETE FROM activity_delivery WHERE student_code IN (SELECT code FROM student WHERE class_code = :class_code);

            DELETE FROM activity_grade WHERE student_code IN (SELECT code FROM student WHERE class_code = :class_code);

            DELETE FROM approval_prediction WHERE student_code IN (SELECT code FROM student WHERE class_code = :class_code);

            DELETE FROM student WHERE class_code = :class_code;

            DELETE FROM material WHERE module_code IN (SELECT code FROM module WHERE class_code = :class_code);

            DELETE FROM module WHERE class_code = :class_code;

            DELETE FROM class WHERE code = :class_code;
        """

        query_db(
            query,
            class_code=class_code,
        )
