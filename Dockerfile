FROM python:3.10.9-slim as system-dependencies

RUN apt update -y
RUN apt install -y libpq-dev build-essential

RUN python -m ensurepip --upgrade
RUN python -m pip install poetry

COPY . /class_management_back
WORKDIR /class_management_back

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8787

