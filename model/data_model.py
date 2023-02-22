from class_management_back.db.config import query_db
from class_management_back.exceptions.log_data import ErrorCreatingClassException, ErrorCreatingModuleException, ErrorCreatingStudentException
from class_management_back.schema.data import Class, Module, Student


class DataModel:
    def create_class(self, name: str, user_code: int):
        query = """
            INSER INTO 
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
            INSER INTO 
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
            INSER INTO 
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
