from typing import Literal
from pandas import DataFrame
import pandas as pd
from class_management_back.helper.user import get_user_from_token
from class_management_back.schema.data import DataUploadParams
from class_management_back.model.data_model import DataModel

data_model = DataModel()

all_modules = [
    'Boas vindas e preparação',
    'Módulo 1',
    'Módulo 2',
    'Módulo 3',
    'Módulo 4',
    'Módulo Bônus',
    'Material extra',
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
            'Boas vindas e preparação': ['Formulário pré-curso', 'aula 1 - Aula', 'aula 2 - Preparação', 'aula 3 - Jupyter'],
            'Módulo 1': ['Módulo 1', 'livro 1', 'aula 4 - Bioinformática', 'aula 5 - Computação', 'aula 6 - Outros conceitos'],
            'Módulo 2': ['livro 2', 'estruturas de repetição', 'Conjuntos', 'Dicionários', 'Listas', 'Tuplas', 'aula 7 - Escolha', 'aula 8 - Primeiro programa', 'Strings', 'aula 9 - Sintaxe', 'aulas 8-9', 'Sintaxe básica', 'aula 10', 'aula 11', 'aula 12', 'Variáveis', 'aula 13', 'aula 14', 'aula 15', 'aula 16', 'aulas 14-16', 'aula 17', 'aula 18', 'aula 19', 'aula 20', 'Operadores', 'aula 21', 'Estruturas condicionais', 'operadores e estruturas condicionais', 'aula 22', 'aula 23', 'aulas 22-23', 'Estruturas de repetição', 'aula 24', 'aula 25', 'aula 26', 'aula 27', 'aula 28', 'aula 29'],
            'Módulo 3': ['livro 3', 'aula 30', 'aula 31', 'aula 32', 'aula 33', 'aula 34', 'aula 35', 'aula 36', 'aula 37', 'aula 38', 'Algoritmos de busca', 'Função Maior'],
            'Módulo 4': ['livro 4', 'aula 39', 'aula 40', 'aula 41', 'aula 42', 'aula 43', 'aula 44', 'aula 45', 'aula 46', 'aula 47'],
            'Módulo Bônus': ['Gravação da aula sobre Bioinformática Estrutural', 'aula 1 - Introdução', 'aula 2 - Fundamentos', 'aula 3 - PDB', 'aula 4 - PDB', 'aula 5 - Modelagem', 'aula 6 - Modelagem', 'aula 7 - Visualização', 'aula 8 - Docking', 'aula 9 - Análise'],
            'Material extra': ['OnlineBioinfo'],
        }

        def identify_module(row):
            for module in modules:
                for substr in modules[module]:
                    if substr in row['Contexto do Evento']:
                        row['modulo'] = module
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
            regex='(Endereço de email)|((.*)Entrega(.*))', axis=1)
        mapa = {
            "Não concluído": True,
            "Concluído": False
        }
        for column in data:
            column = str(column)
            if 'Entrega' in column:
                new_column = 'Exercício Prático - ' + column.split(' - ', 1)[1]
                data[new_column] = data[column].map(mapa).astype('bool')
                del data[column]
        return data

    def _treat_grade_data(self, data: DataFrame):
        data = data.filter(
            regex='(Endereço de email)|(Questionário:(.*)\\(Real\\))', axis=1)

        def isfloat(num):
            try:
                float(num)
                return True
            except ValueError:
                return False

        for column in data:
            column = str(column)
            if 'Questionário' in column:
                new_column = 'Exercício de Revisão - ' + \
                    column.split(' - ', 1)[1][:-7]
                data[new_column] = data[column].apply(
                    lambda x: isfloat(x)).astype('bool')
                del data[column]
        return data

    def _save_class(self, name: str):
        user = get_user_from_token()
        return data_model.create_class(name, user.code)

    def _save_students(self, delivery_data: DataFrame, class_code: int):
        name_email_data = delivery_data[[
            "Endereço de email"]].drop_duplicates()
        return [data_model.create_student(
                str(name), str(row["Endereço de email"]), class_code) for name, row in name_email_data.iterrows()]

    def _save_modules(self, class_code: int):
        return [data_model.create_module(module, class_code) for module in all_modules]

    def _save_materials(self):
        pass

    def _save_material_view(self):
        pass

    def _save_activity_delivery(self):
        pass

    def _save_activity_grade(self):
        pass

    def process_data(
        self,
        log_data: DataFrame,
        delivery_data: DataFrame,
        grade_data: DataFrame,
        args: DataUploadParams,
    ):
        new_class = self._save_class(args.class_name)
        modules = self._save_modules(new_class.code)
        log_data = self._treat_log_data(
            log_data, args.ignore_user_names, args.ignore_activities
        )
        delivery_data = self._treat_delivery_data(delivery_data)
        grade_data = self._treat_grade_data(grade_data)
        new_students = self._save_students(delivery_data, new_class.code)
