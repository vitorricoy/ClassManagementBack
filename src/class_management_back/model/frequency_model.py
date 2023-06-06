from class_management_back.db.config import query_db
from class_management_back.schema.frequency import (
    FrequencyHeatMap,
    FrequencyStudentMean,
    FrequencyWeekMean,
)
from class_management_back.schema.module import ModuleHeatMap
from class_management_back.schema.progress import (
    ProgressMeanStudent,
    ProgressRepetitionMaterial,
    ProgressRepetitionMaterialStudent,
)


class FrequencyModel:
    def get_heatmap(self, class_code: int, user_code: int):
        query = """
            WITH weeks AS (
                SELECT DISTINCT
                    DATE_TRUNC('week', class_view.hour) as week
                FROM
                    class_view
                INNER JOIN
                    student
                ON
                    class_view.student_code = student.code
                INNER JOIN
                    class
                ON
                    student.class_code = class.code
                WHERE
                    class.code = :class_code AND
                    class.user_code = :user_code
            )
            SELECT
                student.name as email,
                TO_CHAR(weeks.week, 'DD/MM/YYYY') as week,
                COUNT(class_view.code) as frequency
            FROM
                student
            CROSS JOIN
                weeks
            LEFT JOIN
                class_view
            ON
                class_view.student_code = student.code AND
                DATE_TRUNC('week', class_view.hour) = weeks.week
            INNER JOIN
                class
            ON
                student.class_code = class.code AND
                class.user_code = :user_code AND
                class.code = :class_code
            GROUP BY
                student.name,
                weeks.week;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [FrequencyHeatMap(**r) for r in result]

    def get_student_mean(self, class_code: int, user_code: int):
        query = """
            WITH weeks AS (
                SELECT DISTINCT
                    DATE_TRUNC('week', class_view.hour) as week
                FROM
                    class_view
                INNER JOIN
                    student
                ON
                    class_view.student_code = student.code
                INNER JOIN
                    class
                ON
                    student.class_code = class.code
                WHERE
                    class.code = :class_code AND
                    class.user_code = :user_code
            ), frequencies AS (
                SELECT
                    student.name as email,
                    TO_CHAR(weeks.week, 'DD/MM/YYYY') as week,
                    COUNT(class_view.code) as frequency
                FROM
                    student
                CROSS JOIN
                    weeks
                LEFT JOIN
                    class_view
                ON
                    class_view.student_code = student.code AND
                    DATE_TRUNC('week', class_view.hour) = weeks.week
                INNER JOIN
                    class
                ON
                    student.class_code = class.code AND
                    class.user_code = :user_code AND
                    class.code = :class_code
                GROUP BY
                    student.name,
                    weeks.week
            )
            SELECT
                frequencies.email,
                AVG(frequencies.frequency) as frequency
            FROM
                frequencies
            GROUP BY
                frequencies.email
            ORDER BY
                frequency DESC;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [FrequencyStudentMean(**r) for r in result]

    def get_week_mean(self, class_code: int, user_code: int):
        query = """
            WITH weeks AS (
                SELECT DISTINCT
                    DATE_TRUNC('week', class_view.hour) as week
                FROM
                    class_view
                INNER JOIN
                    student
                ON
                    class_view.student_code = student.code
                INNER JOIN
                    class
                ON
                    student.class_code = class.code
                WHERE
                    class.code = :class_code AND
                    class.user_code = :user_code
            ), frequencies AS (
                SELECT
                    student.name as email,
                    TO_CHAR(weeks.week, 'DD/MM/YYYY') as week,
                    weeks.week as week_raw,
                    COUNT(class_view.code) as frequency
                FROM
                    student
                CROSS JOIN
                    weeks
                LEFT JOIN
                    class_view
                ON
                    class_view.student_code = student.code AND
                    DATE_TRUNC('week', class_view.hour) = weeks.week
                INNER JOIN
                    class
                ON
                    student.class_code = class.code AND
                    class.user_code = :user_code AND
                    class.code = :class_code
                GROUP BY
                    student.name,
                    weeks.week
            )
            SELECT
                frequencies.week,
                AVG(frequencies.frequency) as frequency
            FROM
                frequencies
            GROUP BY
                frequencies.week, frequencies.week_raw
            ORDER BY
                frequencies.week_raw;
        """
        result = query_db(query, class_code=class_code, user_code=user_code)
        return [FrequencyWeekMean(**r) for r in result]
