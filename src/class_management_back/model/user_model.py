from class_management_back.db.config import query_db
from class_management_back.exceptions.user import (
    AccountAlreadyExistsException,
    CouldNotFindAccountException,
    ErrorCreatingAccountException,
)
from class_management_back.schema.user import User


class UserModel:
    def create(self, name: str, email: str, password: str):
        query = """
            INSERT INTO 
                account (
                    name, 
                    email, 
                    password
                ) 
            VALUES(
                :name, 
                :email, 
                :password
            )
            ON CONFLICT(email) DO NOTHING
            RETURNING *;
        """
        result = query_db(query, name=name, email=email, password=password)
        if not result:
            raise AccountAlreadyExistsException()
        if not result[0]:
            raise ErrorCreatingAccountException()
        return User(**result[0])

    def get_by_email_and_password(self, email: str, password: str):
        query = """
            SELECT
                *
            FROM
                account
            WHERE
                email = :email AND
                password = :password;
        """
        result = query_db(query, email=email, password=password)
        if not result or not result[0]:
            raise CouldNotFindAccountException()
        return User(**result[0])
