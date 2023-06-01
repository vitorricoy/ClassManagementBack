from class_management_back.db.config import query_db
from class_management_back.schema.data import (
    Class,
)


class ClassModel:
    def get_classes(self, user_code: int):
        query = """
            SELECT
                *
            FROM
                class
            WHERE
                user_code = :user_code
            ORDER BY
                code;
        """
        result = query_db(query, user_code=user_code)
        return [Class(**r) for r in result]

    def get_class(self, user_code: int, class_code: int):
        query = """
            SELECT
                *
            FROM
                class
            WHERE
                user_code = :user_code AND code = :class_code
        """
        result = query_db(query, user_code=user_code, class_code=class_code)
        if not result:
            return None
        return Class(**result[0])
