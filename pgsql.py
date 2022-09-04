from constrants import *
import psycopg2 as db
from psycopg2.errors import DatabaseError
from psycopg2._psycopg import _Cursor
from contextlib import contextmanager
import logging

@contextmanager
def get_connection():
    try:
        logging.debug('opening postgres connection: %s', PGSQL_HOST)
        pgsql_conn = db.connect(host=PGSQL_HOST, port=PGSQL_PORT, user=PGSQL_USER, password=PGSQL_PASSWORD, dbname='ddstats')
        pgsql_conn.autocommit = True
        cursor: _Cursor = pgsql_conn.cursor()
        yield cursor
    except DatabaseError as err:
        logging.error(err)
    finally:
        if cursor:
            cursor.close()
        if pgsql_conn:
            pgsql_conn.close()

@contextmanager
def select(stmt=str, args=tuple):
    with get_connection() as cursor:
        cursor.execute(stmt, args)
        yield cursor

def select_all(stmt=str, args=tuple):
    with select(stmt, args) as cursor:
        return cursor.fetchall()


def select_one(stmt=str, args=tuple):
    with select(stmt, args) as cursor:
        return cursor.fetchone()