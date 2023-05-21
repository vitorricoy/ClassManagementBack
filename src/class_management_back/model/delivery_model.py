from class_management_back.db.config import query_db
from class_management_back.schema.delivery import DeliveryActivityCount, DeliveryHeatMap, DeliveryStudentCount


class DeliveryModel:
    def get_delivery_heatmap(self, class_code: int, user_code: int):
        query = """
            wITH deliveries AS (
                SELECT
                    student.email as email,
                    material.name as activity,
                    material.code as material_code,
                    (
                        EXISTS(
                            SELECT 
                                1 
                            FROM 
                                activity_delivery 
                            WHERE 
                                student_code = student.code AND 
                                material_code = material.code
                        )
                    ) as delivered
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
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
                delivered
            FROM
                deliveries
            WHERE
                deliveries.material_code IN (
                    SELECT DISTINCT
                        material_code
                    FROM 
                        deliveries 
                    WHERE 
                        delivered = TRUE
                );
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [DeliveryHeatMap(**r) for r in result]

    def get_delivery_student_count(self, class_code: int, user_code: int):
        query = """
            wITH deliveries AS (
                SELECT
                    student.email as email,
                    material.name as activity,
                    material.code as material_code,
                    (
                        EXISTS(
                            SELECT 
                                1 
                            FROM 
                                activity_delivery 
                            WHERE 
                                student_code = student.code AND 
                                material_code = material.code
                        )
                    ) as delivered
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
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
                SUM(delivered::int) as count
            FROM
                deliveries
            WHERE
                deliveries.material_code IN (
                    SELECT DISTINCT
                        material_code
                    FROM 
                        deliveries 
                    WHERE 
                        delivered = TRUE
                )
            GROUP BY 
                email
            ORDER BY
                count DESC;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [DeliveryStudentCount(**r) for r in result]

    def get_delivery_activity_count(self, class_code: int, user_code: int):
        query = """
            wITH deliveries AS (
                SELECT
                    student.email as email,
                    material.name as activity,
                    material.code as material_code,
                    (
                        EXISTS(
                            SELECT 
                                1 
                            FROM 
                                activity_delivery 
                            WHERE 
                                student_code = student.code AND 
                                material_code = material.code
                        )
                    ) as delivered
                FROM
                    student
                CROSS JOIN
                    material
                INNER JOIN
                    module
                ON
                    module.code = material.module_code
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
                activity,
                SUM(delivered::int) as count
            FROM
                deliveries
            WHERE
                deliveries.material_code IN (
                    SELECT DISTINCT
                        material_code
                    FROM 
                        deliveries 
                    WHERE 
                        delivered = TRUE
                )
            GROUP BY 
                activity
            ORDER BY
                count DESC;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [DeliveryActivityCount(**r) for r in result]
