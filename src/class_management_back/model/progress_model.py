from class_management_back.db.config import query_db
from class_management_back.schema.module import ModuleHeatMap
from class_management_back.schema.progress import ProgressMeanStudent, ProgressRepetitionMaterial, ProgressRepetitionMaterialStudent


class ProgressModel:
    def get_mean_student(self, class_code: int, user_code: int):
        query = """
            WITH views_by_material AS (
                SELECT
                    student.email as email,
                    material.name as material,
                    material.code as material_code,
                    COUNT(material_view.code) as count
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
                INNER JOIN
                    material_view
                ON
                    material_view.student_code = student.code AND
                    material_view.material_code = material.code
                INNER JOIN
                    class
                ON
                    class.user_code = :user_code AND
                    class.code = :class_code
                WHERE
                    student.class_code = :class_code AND
                    module.class_code = :class_code
                GROUP BY
                    student.email, material.name, material.code
            )
            SELECT
                views_by_material.email,
                AVG(views_by_material.count) as repetition
            FROM
                views_by_material
            GROUP BY
                views_by_material.email
            ORDER BY
                repetition DESC;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [ProgressMeanStudent(**r) for r in result]

    def get_repetition_material_student(self, class_code: int, user_code: int):
        query = """
            WITH views_by_material AS (
                SELECT
                    student.email as email,
                    material.name as material,
                    material.code as material_code,
                    COUNT(material_view.code) as count
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
                INNER JOIN
                    material_view
                ON
                    material_view.student_code = student.code AND
                    material_view.material_code = material.code
                INNER JOIN
                    class
                ON
                    class.user_code = :user_code AND
                    class.code = :class_code
                WHERE
                    student.class_code = :class_code AND
                    module.class_code = :class_code
                GROUP BY
                    student.email, material.name, material.code
            ), mean_student_repetition AS (
                SELECT
                    views_by_material.email,
                    AVG(views_by_material.count) as user_mean
                FROM
                    views_by_material
                GROUP BY
                    views_by_material.email
            )
            SELECT
                views_by_material.material,
                views_by_material.email,
                views_by_material.count,
                mean_student_repetition.user_mean
            FROM
                views_by_material
            INNER JOIN
               mean_student_repetition
            ON
               mean_student_repetition.email = views_by_material.email
            ORDER BY
                (views_by_material.count::float/mean_student_repetition.user_mean) DESC;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [ProgressRepetitionMaterialStudent(**r) for r in result]

    def get_repetition_material(self, class_code: int, user_code: int):
        query = """
            WITH views_by_material AS (
                SELECT
                    student.email as email,
                    material.name as material,
                    material.code as material_code,
                    COUNT(material_view.code) as count
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
                INNER JOIN
                    material_view
                ON
                    material_view.student_code = student.code AND
                    material_view.material_code = material.code
                INNER JOIN
                    class
                ON
                    class.user_code = :user_code AND
                    class.code = :class_code
                WHERE
                    student.class_code = :class_code AND
                    module.class_code = :class_code
                GROUP BY
                    student.email, material.name, material.code
            )
            SELECT
                views_by_material.material,
                AVG(views_by_material.count) as count
            FROM
                views_by_material
            GROUP BY
                views_by_material.material
            ORDER BY
                count DESC;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [ProgressRepetitionMaterial(**r) for r in result]
