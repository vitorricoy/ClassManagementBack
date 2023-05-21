from class_management_back.db.config import query_db
from class_management_back.schema.approval import ApprovalProbability


class ApprovalModel:
    def get_probability(self, class_code: int, user_code: int):
        query = """
            SELECT
                student.email,
                approval_prediction.probability * 100 as probability
            FROM
                approval_prediction
            INNER JOIN
                student
            ON
                student.code = approval_prediction.student_code
            INNER JOIN
                class
            ON
                class.code = student.class_code
            WHERE
                class.user_code = :user_code AND
                class.code = :class_code
            ORDER BY
                probability DESC;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [ApprovalProbability(**r) for r in result]
