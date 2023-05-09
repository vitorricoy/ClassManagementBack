CREATE DATABASE class_management;

CREATE TABLE account (
    code serial PRIMARY KEY,
    name text NOT NULL, 
    email text NOT NULL, 
    password text NOT NULL
);

CREATE TABLE class (
    code serial PRIMARY KEY,
    name text NOT NULL,
    user_code int REFERENCES account(code) NOT NULL
);

CREATE TABLE student (
    code serial PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    class_code int REFERENCES class(code) NOT NULL
);

CREATE TABLE module (
    code serial PRIMARY KEY,
    name text NOT NULL,
    class_code int REFERENCES class(code) NOT NULL
);

CREATE TABLE material (
    code serial PRIMARY KEY,
    name text NOT NULL,
    module_code int REFERENCES module(code) NOT NULL
);

CREATE TABLE class_view (
    code serial PRIMARY KEY,
    student_code int REFERENCES student(code) NOT NULL,
    hour timestamptz NOT NULL
);

CREATE TABLE material_view (
    code serial PRIMARY KEY,
    student_code int REFERENCES student(code) NOT NULL,
    material_code int REFERENCES material(code) NOT NULL,
    hour timestamptz NOT NULL
);

CREATE TABLE activity_delivery (
    code serial PRIMARY KEY,
    student_code int REFERENCES student(code) NOT NULL,
    material_code int REFERENCES material(code) NOT NULL
);

CREATE TABLE activity_grade (
    code serial PRIMARY KEY,
    student_code int REFERENCES student(code) NOT NULL,
    material_code int REFERENCES material(code) NOT NULL,
    grade float NOT NULL
);

CREATE TABLE approval_prediction (
    code serial PRIMARY KEY,
    student_code int REFERENCES student(code) NOT NULL,
    probability float NOT NULL
);

CREATE UNIQUE INDEX ON account(email);