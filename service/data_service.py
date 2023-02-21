from pandas import DataFrame

from class_management_back.schema.data import DataUploadParams


class DataService:
    def process_data(
        self,
        log_data: DataFrame,
        delivery_data: DataFrame,
        grade_data: DataFrame,
        args: DataUploadParams,
    ):
        pass
