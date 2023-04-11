from contextlib import contextmanager
from typing import Any, TypeVar
from pydantic import BaseModel, parse_obj_as

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker, scoped_session

from class_management_back.src.class_management_back.environment import DB_URI

M = TypeVar("M", bound=BaseModel)


class DbPool:
    def __init__(self, engine):
        self.engine = engine

    def _execute(self, sql, conn, *args, **kwargs):
        statement = sql if args else text(sql)
        result = conn.execute(statement, *args, **kwargs)
        return [dict(i.items()) for i in result]

    def query(self, sql, conn=None, *args, **kwargs) -> list[dict[str, Any]]:
        if conn:
            return self._execute(sql, conn, *args, **kwargs)

        with self.engine.connect() as conn:
            with conn.begin():
                return self._execute(sql, conn, **kwargs)

    def connection(self):
        return self.engine.connect()

    def model_query(
        self, sql: str, model: type[M], *args, conn=None, **kwargs: Any
    ):
        return parse_obj_as(
            list[model], self.query(sql, conn, *args, **kwargs)
        )

    @contextmanager
    def transaction(self):
        with self.engine.connect() as conn, conn.begin():
            yield conn

    @contextmanager
    def idempotent_transaction(self, conn):
        if isinstance(conn, Connection):
            yield conn
        elif conn is None:
            with self.transaction() as conn:
                yield conn
        else:
            raise TypeError(f"Bad conn: {conn}")


engine = create_engine(DB_URI, client_encoding="utf-8", pool_recycle=3600)

Session = scoped_session(sessionmaker(bind=engine))


def _query(engine_obj, sql, conn=None, *args, **kwargs):
    # Positional arguments only work without kwargs.
    query = sql if args else text(sql)

    if conn:
        result = conn.execute(query, *args, **kwargs)
        return [dict(i.items()) for i in result]

    conn = engine_obj.connect()
    try:
        with conn.begin():
            result = conn.execute(query, *args, **kwargs)
            result = [dict(i.items()) for i in result]
    except Exception as e:
        raise e
    finally:
        conn.close()

    return result


def query_db(sql, conn=None, *args, **kwargs):
    return _query(engine, sql, conn, *args, **kwargs)
