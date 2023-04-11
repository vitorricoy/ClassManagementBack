from typing import Literal
from pandas import DataFrame
import pandas as pd
from class_management_back.exceptions.log_data import (
    InvalidMaterialName,
    InvalidStudentEmail,
    InvalidStudentName,
    InvalidModuleName,
)
from class_management_back.helper.user import get_user_from_token
from class_management_back.schema.data import (
    DataUploadParams,
    Material,
    Module,
    Student,
)
from class_management_back.model.data_model import DataModel

data_model = DataModel()

all_modules = [
    "Boas vindas e preparação",
    "Módulo 1",
    "Módulo 2",
    "Módulo 3",
    "Módulo 4",
    "Módulo Bônus",
    "Material extra",
]


class DataService:
    def _handle_operations_in_behalf(self, data: DataFrame):
        if " como " in data["Nome completo"]:
            data["Nome completo"] = data["Nome completo"].split(" como ")[1]
        return data

    def _handle_automatic_operations(self, data: DataFrame):
        if data["Usuário afetado"] != "-":
            data["Nome completo"] = data["Usuário afetado"]
        return data

    def _assign_modules(self, data: DataFrame):
        modules = {
            "Boas vindas e preparação": [
                "Formulário pré-curso",
                "aula 1 - Aula",
                "aula 2 - Preparação",
                "aula 3 - Jupyter",
            ],
            "Módulo 1": [
                "Módulo 1",
                "livro 1",
                "aula 4 - Bioinformática",
                "aula 5 - Computação",
                "aula 6 - Outros conceitos",
            ],
            "Módulo 2": [
                "livro 2",
                "estruturas de repetição",
                "Conjuntos",
                "Dicionários",
                "Listas",
                "Tuplas",
                "aula 7 - Escolha",
                "aula 8 - Primeiro programa",
                "Strings",
                "aula 9 - Sintaxe",
                "aulas 8-9",
                "Sintaxe básica",
                "aula 10",
                "aula 11",
                "aula 12",
                "Variáveis",
                "aula 13",
                "aula 14",
                "aula 15",
                "aula 16",
                "aulas 14-16",
                "aula 17",
                "aula 18",
                "aula 19",
                "aula 20",
                "Operadores",
                "aula 21",
                "Estruturas condicionais",
                "operadores e estruturas condicionais",
                "aula 22",
                "aula 23",
                "aulas 22-23",
                "Estruturas de repetição",
                "aula 24",
                "aula 25",
                "aula 26",
                "aula 27",
                "aula 28",
                "aula 29",
            ],
            "Módulo 3": [
                "livro 3",
                "aula 30",
                "aula 31",
                "aula 32",
                "aula 33",
                "aula 34",
                "aula 35",
                "aula 36",
                "aula 37",
                "aula 38",
                "Algoritmos de busca",
                "Função Maior",
            ],
            "Módulo 4": [
                "livro 4",
                "aula 39",
                "aula 40",
                "aula 41",
                "aula 42",
                "aula 43",
                "aula 44",
                "aula 45",
                "aula 46",
                "aula 47",
            ],
            "Módulo Bônus": [
                "Gravação da aula sobre Bioinformática Estrutural",
                "aula 1 - Introdução",
                "aula 2 - Fundamentos",
                "aula 3 - PDB",
                "aula 4 - PDB",
                "aula 5 - Modelagem",
                "aula 6 - Modelagem",
                "aula 7 - Visualização",
                "aula 8 - Docking",
                "aula 9 - Análise",
            ],
            "Material extra": ["OnlineBioinfo"],
        }

        def identify_module(row):
            for module in modules:
                for substr in modules[module]:
                    if substr in row["Contexto do Evento"]:
                        row["modulo"] = module
                        return row

        return data.apply(identify_module, axis=1)

    def _treat_log_data(
        self,
        data: DataFrame,
        ignored_users: list[str],
        ignored_activities: list[str],
    ):
        data["Hora"] = pd.to_datetime(data["Hora"], format="%d/%m/%Y %H:%M")
        data = data.apply(
            self._handle_operations_in_behalf, axis=1
        )  # type: ignore
        data = data.apply(
            self._handle_automatic_operations, axis=1
        )  # type: ignore

        for ignored_user in ignored_users:
            data = data[data["Nome completo"] != ignored_user]

        data = data[data["Nome completo"] != "-"]

        data = data[~data["Contexto do Evento"].isin(ignored_activities)]

        data = self._assign_modules(data)  # type: ignore
        return data

    def _treat_delivery_data(self, data: DataFrame):
        data = data.filter(
            regex="(Endereço de email)|((.*)Entrega(.*))", axis=1
        )
        mapa = {"Não concluído": True, "Concluído": False}
        for column in data:
            column = str(column)
            if "Entrega" in column:
                data[column] = data[column].map(mapa).astype("bool")
        return data

    def _treat_grade_data(self, data: DataFrame):
        data = data.filter(
            regex="(Endereço de email)|(Questionário:(.*)\\(Real\\))", axis=1
        )

        def isfloat(num):
            try:
                float(num)
                return True
            except ValueError:
                return False

        for column in data:
            column = str(column)
            if "Questionário" in column:
                new_column = (
                    column.replace('Questionário: ', '')
                )
                data[new_column] = (
                    data[column].apply(lambda x: isfloat(x)).astype("bool")
                )
                del data[column]
        return data

    def _save_class(self, name: str):
        user = get_user_from_token()
        return data_model.create_class(name, user.code)

    def _save_students(self, delivery_data: DataFrame, class_code: int):
        name_email_data = delivery_data[
            ["Endereço de email"]
        ].drop_duplicates()
        return [
            data_model.create_student(
                str(name), str(row["Endereço de email"]), class_code
            )
            for name, row in name_email_data.iterrows()
        ]

    def _save_modules(self, class_code: int):
        return [
            data_model.create_module(module, class_code)
            for module in all_modules
        ]

    def _get_module_code_by_name(self, name: str, modules: list[Module]):
        first_or_default = next(
            (
                module
                for module in modules
                if module.name.lower() == name.lower()
            ),
            None,
        )
        if first_or_default:
            return first_or_default.code
        raise InvalidModuleName(name)

    def _get_student_code_by_name(self, name: str, students: list[Student]):
        first_or_default = next(
            (
                student
                for student in students
                if student.name.lower() == name.lower()
            ),
            None,
        )
        if first_or_default:
            return first_or_default.code
        raise InvalidStudentName(name)

    def _get_student_code_by_email(self, email: str, students: list[Student]):
        first_or_default = next(
            (
                student
                for student in students
                if student.email.lower() == email.lower()
            ),
            None,
        )
        if first_or_default:
            return first_or_default.code
        raise InvalidStudentEmail(email)

    def _get_material_code_by_name(self, name: str, materials: list[Material]):
        first_or_default = next(
            (
                material
                for material in materials
                if material.name.lower() == name.lower()
            ),
            None,
        )
        if first_or_default:
            return first_or_default.code
        raise InvalidMaterialName(name)

    def _is_valid_activity(self, name: str):
        return name.startswith('Arquivo: ') or name.startswith('Questionário: ') or name.startswith('Tarefa: ') or name.startswith('URL: ')

    def _get_activity_name(self, name: str):
        names = name.split(':')
        return ':'.join(names[1:])

    def _save_materials(self, modules: list[Module], log_data: DataFrame):
        events_modules_data = log_data[
            ["Contexto do Evento", "modulo"]
        ].drop_duplicates()
        return [
            data_model.create_material(
                self._get_activity_name(row["Contexto do Evento"]),
                self._get_module_code_by_name(row["modulo"], modules),
            )
            for _, row in events_modules_data.iterrows()
            if self._is_valid_activity(row["Contexto do Evento"])
        ]

    def _save_material_view(
        self,
        materials: list[Material],
        students: list[Student],
        log_data: DataFrame,
    ):
        events_modules_data = log_data[
            ["Contexto do Evento", "Nome completo",
                "Nome do evento", "modulo", "Hora"]
        ].drop_duplicates()
        return [
            data_model.create_material_view(
                self._get_material_code_by_name(
                    self._get_activity_name(row["Contexto do Evento"]),
                    materials,
                ),
                self._get_student_code_by_name(row["Nome completo"], students),
                row["Hora"],
            )
            for _, row in events_modules_data.iterrows()
            if row["Nome do evento"] == "Módulo do curso visualizado"
        ]

    def _save_class_view(
        self,
        students: list[Student],
        log_data: DataFrame,
    ):
        events_modules_data = log_data[
            ["Contexto do Evento", "Nome completo",
                "Nome do evento", "modulo", "Hora"]
        ].drop_duplicates()
        return [
            data_model.create_class_view(
                self._get_student_code_by_name(row["Nome completo"], students),
                row["Hora"],
            )
            for _, row in events_modules_data.iterrows()
            if row["Nome do evento"] == "Curso visto"
        ]

    def _save_activity_delivery(self, students: list[Student], materials: list[Material], delivery_data: DataFrame):
        return [
            data_model.create_activity_delivery(
                self._get_student_code_by_email(
                    str(row["Endereço de email"]), students),
                self._get_material_code_by_name(str(column), materials),
            )
            for _, row in delivery_data.iterrows()
            for column in delivery_data if '@' not in str(column) if row[column]
        ]

    def _save_activity_grade(self, students: list[Student], materials: list[Material], grade_data: DataFrame):
        return [
            data_model.create_activity_grade(
                self._get_student_code_by_email(
                    str(row["Endereço de email"]), students),
                self._get_material_code_by_name(str(column), materials),
                float(str(row[column])),
            )
            for _, row in grade_data.iterrows()
            for column in grade_data if '@' not in str(column)
        ]

    def process_data(
        self,
        log_data: DataFrame,
        delivery_data: DataFrame,
        grade_data: DataFrame,
        args: DataUploadParams,
    ):
        new_class = self._save_class(args.class_name)
        log_data = self._treat_log_data(
            log_data, args.ignore_user_names, args.ignore_activities
        )
        delivery_data = self._treat_delivery_data(delivery_data)
        grade_data = self._treat_grade_data(grade_data)
        modules = self._save_modules(new_class.code)
        materials = self._save_materials(modules, log_data)
        students = self._save_students(delivery_data, new_class.code)
        self._save_class_view(students, log_data)
        self._save_material_view(
            materials, students, log_data
        )
        self._save_activity_delivery(students, materials, delivery_data)
        self._save_activity_grade(students, materials, grade_data)
