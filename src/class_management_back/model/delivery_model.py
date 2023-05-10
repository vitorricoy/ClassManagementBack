from class_management_back.db.config import query_db
from class_management_back.schema.delivery import DeliveryHeatMap


class DeliveryModel:
    def get_delivery_heatmap(self, name: str, user_code: int):
        query = """
            SELECT
                student.email as email,
                material.name as activity,
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
            WHERE
                student.class_code = :class_code AND
                module.class_code = :class_code;
        """
        result = query_db(query, name=name, user_code=user_code)
        return [DeliveryHeatMap(**r) for r in result]
