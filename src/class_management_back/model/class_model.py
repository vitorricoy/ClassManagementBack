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
        """
        result = query_db(query, user_code=user_code)
        return [Class(**r) for r in result]
