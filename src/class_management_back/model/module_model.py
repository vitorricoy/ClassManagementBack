from class_management_back.db.config import query_db
from class_management_back.schema.delivery import (
    DeliveryActivityCount,
    DeliveryStudentCount,
)
from class_management_back.schema.grade import GradeHeatMap, GradeStudent
from class_management_back.schema.module import ModuleHeatMap


class ModuleModel:
    def get_module_heatmap(self, class_code: int, user_code: int):
        query = """
            WITH module_conclusion AS (
                SELECT
                    student.email as email,
                    module.name as module,
                    module.code as module_code,
                    SUM(CASE WHEN material_seen.seen IS NULL THEN 0 ELSE 1 END) as count
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
                LEFT JOIN LATERAL (
					SELECT
						COUNT(*) as seen
					FROM
						material_view
					WHERE
						material_view.student_code = student.code AND
						material_view.material_code = material.code
                    GROUP BY
                        material_view.material_code
				) as material_seen
                ON 
                    TRUE
                INNER JOIN
                    class
                ON
                    student.class_code = class.code AND
                    class.user_code = :user_code AND
                    class.code = :class_code
                GROUP BY
                    student.email, module.name, module.code
            ), module_total_view AS (
                SELECT
                    module.code as module_code,
                    COUNT(material.code) as count
                FROM
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
                INNER JOIN
                    class
                ON
                    module.class_code = class.code AND
                    class.code = module.class_code AND
                    class.user_code = :user_code
                WHERE
                    class.code = :class_code
                GROUP BY
                    module.code
            )
            SELECT
                module_conclusion.email,
                module_conclusion.module,
                (module_conclusion.count::float/module_total_view.count)*100 as conclusion
            FROM
                module_conclusion
            INNER JOIN
                module_total_view
            ON
                module_total_view.module_code = module_conclusion.module_code;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [ModuleHeatMap(**r) for r in result]
