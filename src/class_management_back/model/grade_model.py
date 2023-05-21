from class_management_back.db.config import query_db
from class_management_back.schema.delivery import DeliveryActivityCount, DeliveryStudentCount
from class_management_back.schema.grade import GradeHeatMap, GradeStudent


class GradeModel:
    def get_grade_heatmap(self, class_code: int, user_code: int):
        query = """
            WITH grades AS (
                SELECT
                    student.email as email,
                    material.name as activity,
                    material.code as material_code,
                    COALESCE(activity_grade.grade, 0) as grade
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
                LEFT JOIN
                    activity_grade
                ON
                    activity_grade.student_code = student.code AND
                    activity_grade.material_code = material.code
                INNER JOIN
                    class
                ON
                    class.user_code = :user_code AND
                    class.code = :class_code
                WHERE
                    student.class_code = :class_code AND
                    module.class_code = :class_code
            )
            SELECT
                email,
                activity,
                grade
            FROM
                grades
            WHERE
                material_code IN (
                    SELECT DISTINCT
                        material_code
                    FROM 
                        grades 
                    WHERE 
                        grade <> 0
                );
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [GradeHeatMap(**r) for r in result]

    def get_grade_student(self, class_code: int, user_code: int):
        query = """
            WITH grades AS (
                SELECT
                    student.email as email,
                    material.name as activity,
                    material.code as material_code,
                    COALESCE(activity_grade.grade, 0) as grade
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
                LEFT JOIN
                    activity_grade
                ON
                    activity_grade.student_code = student.code AND
                    activity_grade.material_code = material.code
                INNER JOIN
                    class
                ON
                    class.user_code = :user_code AND
                    class.code = :class_code
                WHERE
                    student.class_code = :class_code AND
                    module.class_code = :class_code
            ), grade_max AS (
                SELECT
                    material_code,
                    MAX(grade) as max_grade
                FROM
                    activity_grade
                INNER JOIN
                    student
                ON
                    student.code = activity_grade.student_code
                INNER JOIN
                    material
                ON
                    material.code = activity_grade.material_code
                INNER JOIN 
                    module
                ON
                    module.code = material.module_code
                INNER JOIN
                    class
                ON
                    class.code = module.class_code AND
                    class.user_code = :user_code
                WHERE
                    class.code = :class_code
                GROUP BY
                    material_code
            )
            SELECT
                grades.email,
                AVG((grades.grade/grade_max.max_grade)*100) as grade
            FROM
                grades
            INNER JOIN
                grade_max
            ON
                grade_max.material_code = grades.material_code
            WHERE
                grades.material_code IN (
                    SELECT DISTINCT
                        material_code
                    FROM 
                        grades 
                    WHERE 
                        grade <> 0
                )
            GROUP BY
                grades.email
            ORDER BY
                grade DESC;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [GradeStudent(**r) for r in result]
