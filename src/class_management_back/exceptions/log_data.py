class ErrorCreatingClassException(Exception):
    pass


class ErrorCreatingStudentException(Exception):
    pass


class ErrorCreatingModuleException(Exception):
    pass


class ErrorCreatingMaterialException(Exception):
    pass


class ErrorCreatingMaterialViewException(Exception):
    pass


class ErrorCreatingClassViewException(Exception):
    pass


class ErrorCreatingActivityDeliveryException(Exception):
    pass


class ErrorCreatingActivityGradeException(Exception):
    pass


class ErrorCreatingPredictionException(Exception):
    pass


class InvalidModuleName(Exception):
    def __init__(self, name: str):
        super().__init__(f"No module with the name: {name} found")


class InvalidStudentName(Exception):
    def __init__(self, name: str):
        super().__init__(f"No student with the name: {name} found")


class InvalidStudentEmail(Exception):
    def __init__(self, email: str):
        super().__init__(f"No student with the email: {email} found")


class InvalidMaterialName(Exception):
    def __init__(self, name: str):
        super().__init__(f"No material with the name: {name} found")
