import re
from typing import Literal
from pandas import DataFrame
import pandas as pd
from class_management_back.exceptions.log_data import (
    InvalidMaterialName,
    InvalidStudentEmail,
    InvalidStudentName,
    InvalidModuleName,
)
from class_management_back.helper.user import get_user_from_token_with_location
from class_management_back.schema.data import (
    DataUploadParams,
    Material,
    Module,
    Student,
)
from class_management_back.model.data_model import DataModel
import numpy as np
from joblib import load

data_model = DataModel()


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


predictions = load("model.joblib")

all_modules = [
    "Boas vindas e preparação",
    "Módulo 1",
    "Módulo 2",
    "Módulo 3",
    "Módulo 4",
    "Módulo Bônus",
    "Material extra",
]

blacklist = [
    "Dúvidas",
    "Avaliação final",
    "FORMATURA",
    "Desafio - Função Maior",
    "Desafio - Função MaiorMenor",
    "Desafio - Função MaiorMenor3",
    "Desafios - Algoritmos de busca",
    "Exercícios práticos - Sintaxe básica",
    "Exercícios práticos - Sintaxe básica.1",
    "Resolução dos exercícios - Sintaxe básica",
    "Notebook da resolução dos exercícios - Sintaxe básica",
    "Exercícios práticos - Strings",
    "Exercícios práticos - Variáveis - Strings",
    "Resolução dos exercícios - Variáveis - Strings",
    "Notebook da resolução dos exercícios - Variáveis - Strings",
    "Exercícios práticos - Tuplas",
    "Exercícios práticos - Variáveis - Tuplas",
    "Resolução dos exercícios - Variáveis - Tuplas",
    "Notebook da resolução dos exercícios - Tuplas",
    "Exercícios práticos - Listas",
    "Exercícios práticos - Variáveis - Listas",
    "Resolução dos exercícios - Variáveis - Listas",
    "Notebook da resolução dos exercícios - Variáveis - Listas",
    "2022-09-01 07:59:00.1",
    "2022-09-01 07:59:00",
    "2022-09-01 07:59:00.2",
    "Exercícios práticos - Conjuntos",
    "Exercícios práticos - Variáveis - Conjuntos",
    "Resolução dos exercícios - Variáveis - Conjuntos",
    "Notebook da resolução dos exercícios - Variáveis - Conjuntos",
    "Exercícios práticos - Dicionários",
    "Exercícios práticos - Variáveis - Dicionários",
    "Resolução dos exercícios - Variáveis - Dicionários",
    "Notebook da resolução dos exercícios - Variáveis - Dicionários",
    "Exercícios práticos - Operadores",
    "Exercícios práticos - Operadores.1",
    "Resolução dos exercícios - Operadores",
    "Notebook da resolução dos exercícios - Operadores",
    "Exercícios práticos - Operadores - Desafio",
    "Exercícios práticos - Operadores - Desafio.1",
    "Resolução dos exercícios - Operadores - Desafio",
    "Notebook da resolução dos exercícios - Operadores - Desafio",
    "Exercícios práticos - Estruturas condicionais",
    "Exercícios práticos - Estruturas condicionais.1",
    "Resolução dos exercícios - Estruturas condicionais",
    "Notebook da resolução dos exercícios - Estruturas condicionais",
    "Exercícios práticos - Estruturas condicionais - Desafio",
    "Exercícios práticos - Estruturas condicionais - Desafio.1",
    "Resolução dos exercícios - Estruturas condicionais - Desafio",
    "Notebook da resolução dos exercícios - Estruturas condicionais - Desafio",
    "Monitoria (gravada) sobre operadores e estruturas condicionais",
    "Notebook da monitoria sobre operadores e estruturas condicionais",
    "Exercícios práticos - Estruturas de repetição",
    "Exercícios práticos - Estruturas de repetição.1",
    "Resolução dos exercícios - Estruturas de repetição",
    "Notebook da resolução dos exercícios - Estruturas de repetição",
    "Exercícios práticos - Estruturas de repetição - Desafio",
    "Exercícios práticos - Estruturas de repetição - Desafio.1",
    "Resolução dos exercícios - Estruturas de repetição - Desafio",
    "Notebook da resolução dos exercícios - Estruturas de repetição - Desafio",
    "Monitoria (gravada) sobre estruturas de repetição",
    "Notebook da monitoria sobre estruturas de repetição",
    "Formulário pré-curso",
    "Cronograma",
    "Projeto OnlineBioinfo",
    "Canal do YouTube OnlineBioinfo",
    "Perfil no Instagram OnlineBioinfo",
    "Página no LinkedIn do OnlineBioinfo",
    "Gravação da aula sobre Bioinformática Estrutural",
    "aula 1 - Introdução",
    "aula 2 - Fundamentos",
    "aula 3 - PDB",
    "aula 4 - PDB",
    "aula 5 - Modelagem comparativa",
    "aula 6 - Modelagem threading",
    "aula 7 - Visualização molecular",
    "aula 8 - Docking molecular",
    "aula 9 - Análise de interações",
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
            if row["Nome do evento"] == "Curso visto":
                row["modulo"] = "dummy"
                return row
            if row["Nome do evento"] != "Módulo do curso visualizado":
                row["modulo"] = None
                return row
            for module in modules:
                for substr in modules[module]:
                    if substr in row["Contexto do Evento"]:
                        row["modulo"] = module
                        return row
                    if row["Nome do evento"] == "Curso visto":
                        row["modulo"] = "dummy"
            row["modulo"] = None
            return row

        data = data.apply(identify_module, axis=1)
        return data[data["modulo"].notnull()]

    def _treat_log_data(
        self,
        data: DataFrame,
        ignored_users: list[str],
        ignored_activities: list[str],
    ):
        hour_column = str(data.columns[data.columns.str.endswith("Hora")][0])
        data["Hora"] = data[hour_column]
        del data[hour_column]
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
                new_column = "Exercício Prático - " + column.split(" - ", 1)[1]
                data[new_column] = data[column].map(mapa).astype("bool")
                del data[column]
        return data

    def _treat_grade_data(self, data: DataFrame):
        data = data.filter(
            regex="Nome|Sobrenome|(Endereço de email)|(Questionário:(.*)\\(Real\\))",
            axis=1,
        )

        def isfloat(num):
            try:
                float(num)
                return True
            except ValueError:
                return False

        name_column = (data["Nome"] + " " + data["Sobrenome"]).copy()
        for column in data:
            column = str(column)
            if "Questionário" in column:
                new_column = column.replace("Questionário: ", "").replace(
                    " (Real)", ""
                )
                data[new_column] = data[column]
                del data[column]
        del data["Sobrenome"]
        data["Nome"] = name_column
        return data

    def _save_class(self, name: str):
        user = get_user_from_token_with_location(location="form")
        return data_model.create_class(name, user.code)

    def _save_students(self, delivery_data: DataFrame, class_code: int):
        name_email_data = delivery_data[
            ["Endereço de email", "Nome"]
        ].drop_duplicates()
        return [
            data_model.create_student(
                str(row["Nome"]), str(row["Endereço de email"]), class_code
            )
            for _, row in name_email_data.iterrows()
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
        return None

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
        return None

    def _get_material_code_by_name(self, name: str, materials: list[Material]):
        first_or_default = next(
            (
                material
                for material in materials
                if material.name.lower() == name.strip().lower()
            ),
            None,
        )
        if first_or_default:
            return first_or_default.code
        return None

    def _is_valid_activity(self, name: str):
        return (
            name.startswith("Arquivo: ")
            or name.startswith("Questionário: ")
            or name.startswith("Tarefa: ")
            or name.startswith("URL: ")
        )

    def _get_activity_name(self, name: str):
        names = name.split(":")
        new_name = ":".join(names[1:])

        if "Entrega" in new_name:
            return "Exercício Prático - " + new_name.split(" - ", 1)[1]
        return new_name

    def _save_materials(self, modules: list[Module], log_data: DataFrame):
        events_modules_data = log_data[["Contexto do Evento", "modulo"]].copy()
        events_modules_data = events_modules_data.drop_duplicates()
        return [
            data_model.create_material(
                self._get_activity_name(row["Contexto do Evento"]).strip(),
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
            [
                "Contexto do Evento",
                "Nome completo",
                "Nome do evento",
                "modulo",
                "Hora",
            ]
        ].copy()
        events_modules_data = events_modules_data.drop_duplicates()
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
            and self._get_student_code_by_name(row["Nome completo"], students)
            and self._get_material_code_by_name(
                self._get_activity_name(row["Contexto do Evento"]),
                materials,
            )
        ]

    def _save_class_view(
        self,
        students: list[Student],
        log_data: DataFrame,
    ):
        events_modules_data = log_data[
            [
                "Nome completo",
                "Nome do evento",
                "Hora",
            ]
        ].copy()
        events_modules_data = events_modules_data.drop_duplicates()
        return [
            data_model.create_class_view(
                self._get_student_code_by_name(row["Nome completo"], students),
                row["Hora"],
            )
            for _, row in events_modules_data.iterrows()
            if row["Nome do evento"] == "Curso visto"
            and self._get_student_code_by_name(row["Nome completo"], students)
        ]

    def _save_activity_delivery(
        self,
        students: list[Student],
        materials: list[Material],
        delivery_data: DataFrame,
        grade_data: DataFrame,
    ):
        return [
            data_model.create_activity_delivery(
                self._get_material_code_by_name(str(column), materials),
                self._get_student_code_by_email(
                    str(row["Endereço de email"]), students
                ),
            )
            for _, row in delivery_data.iterrows()
            for column in delivery_data
            if "email" not in str(column)
            if row[column]
            and self._get_student_code_by_email(
                str(row["Endereço de email"]), students
            )
            and self._get_material_code_by_name(str(column), materials)
        ] + [
            data_model.create_activity_delivery(
                self._get_material_code_by_name(str(column), materials),
                self._get_student_code_by_email(
                    str(row["Endereço de email"]), students
                ),
            )
            for _, row in grade_data.iterrows()
            for column in grade_data
            if "email" not in str(column) and "Nome" not in str(column)
            if row[column]
            and isfloat(row[column])
            and self._get_student_code_by_email(
                str(row["Endereço de email"]), students
            )
            and self._get_material_code_by_name(str(column), materials)
        ]

    def _save_activity_grade(
        self,
        students: list[Student],
        materials: list[Material],
        grade_data: DataFrame,
    ):
        return [
            data_model.create_activity_grade(
                self._get_material_code_by_name(str(column), materials),
                self._get_student_code_by_email(
                    str(row["Endereço de email"]), students
                ),
                float(row[column]),
            )
            for _, row in grade_data.iterrows()
            for column in grade_data
            if "email" not in str(column)
            and "Nome" not in str(column)
            and isfloat(row[column])
            and self._get_student_code_by_email(
                str(row["Endereço de email"]), students
            )
            and self._get_material_code_by_name(str(column), materials)
        ]

    def _process_prediction_data(self, delivery_data: DataFrame):
        df = delivery_data[
            delivery_data["Endereço de email"] != "nailtonjr@gmail.com"
        ].copy()
        df = df.drop(df.filter(regex="^(Unnamed*)", axis=1).columns, axis=1)
        df_temp = df.copy()
        for column in df.columns:
            new_column = re.sub("[\(\[].*?[\)\]]", "", column).strip()
            df_temp[new_column] = df[column]
            if new_column != column:
                del df_temp[column]
        df = df_temp

        mapa = {"Não concluído": True, "Concluído": False}

        for column in df:
            if column != "Endereço de email":
                df[column] = df[column].map(mapa).astype("bool")
            if "Entrega" in column:
                new_column = "Exercício Prático - " + column.split(" - ", 1)[1]
                df[new_column] = df[column]
                del df[column]
            if column in blacklist or re.match(
                "\d{4}-\d\d-\d\d \d\d:\d\d:\d\d(.\d)*", column
            ):
                del df[column]

        exs = [
            "Exercícios de revisão - Sintaxe básica",
            "Exercícios de revisão - Variáveis - Parte I",
            "Exercícios de revisão - Variáveis - Parte II",
            "Exercícios de revisão - Módulo 1",
            "Exercício Prático - Sintaxe básica",
            "Exercício Prático - Strings",
            "Exercício Prático - Tuplas",
            "Exercício Prático - Listas",
            "Exercício Prático - Conjuntos",
            "Exercício Prático - Dicionários",
            "Exercício Prático -  Operadores",
            "Exercício Prático -  Operadores - Desafio",
            "Exercício Prático -  Estruturas condicionais",
            "Exercício Prático -  Estruturas condicionais - Desafio",
            "Exercício Prático -  Estruturas de repetição",
            "Exercício Prático -  Estruturas de repetição - Desafio",
        ]

        df = df.set_index("Endereço de email")

        df_exs = df.copy()
        df_ativ = df.copy()

        for column in df:
            if column in exs:
                del df_ativ[column]
            else:
                del df_exs[column]

        def calc_perc(row):
            acc = 0
            for column in row:
                if type(column) == bool:
                    acc += column
            acc /= len(row)
            row["perc"] = acc
            return row

        df_ativ = df_ativ.apply(calc_perc, axis=1)
        df_ativ_perc = df_ativ[["perc"]]

        df_exs = df_exs.apply(calc_perc, axis=1)
        df_exs_perc = df_exs[["perc"]]

        df_ativ_perc["passou"] = df_ativ_perc["perc"] > 0.75
        df_exs_perc["passou"] = df_exs_perc["perc"] > 0.6

        linhas = []
        for email in df_ativ_perc.index:
            passou = (
                df_ativ_perc.loc[email].passou
                and df_exs_perc.loc[email].passou
            )
            linha = {"email": email, "passou": passou}
            linhas.append(linha)
        df2 = pd.DataFrame.from_dict(linhas)
        df2 = df2.set_index("email")
        df3 = pd.concat([df2, df], axis=1)
        return df3

    def _save_predictions(
        self, delivery_data: DataFrame, students: list[Student]
    ):
        df = self._process_prediction_data(delivery_data)
        emails = df.index.values.tolist()
        arr = df.to_numpy()
        num_activ = 0
        for i in range(arr.shape[1]):
            if np.any(arr[:, i]):
                num_activ = i + 1
        X_data = arr[:, 1 : num_activ + 1]

        prediction = predictions[num_activ - 1].predict_proba(X_data)[:, 1]
        for i, v in enumerate(prediction):
            if self._get_student_code_by_email(emails[i], students):
                data_model.create_approval_prediction(
                    self._get_student_code_by_email(emails[i], students),
                    v,
                )

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
        original_delivery_data = delivery_data.copy()
        delivery_data = self._treat_delivery_data(delivery_data)
        grade_data = self._treat_grade_data(grade_data)
        modules = self._save_modules(new_class.code)
        materials = self._save_materials(modules, log_data)
        students = self._save_students(grade_data, new_class.code)
        self._save_class_view(students, log_data)
        self._save_material_view(materials, students, log_data)
        self._save_activity_delivery(
            students, materials, delivery_data, grade_data
        )
        self._save_activity_grade(students, materials, grade_data)
        self._save_predictions(original_delivery_data, students)
        return new_class
