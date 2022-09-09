from contextlib import contextmanager
import psycopg2 as db
from psycopg2 import DatabaseError
from psycopg2.extras import _cursor as Cursor
from log import logger as logging
from constrants import *


@contextmanager
def get_connection():
    cursor = None
    pgsql_conn = None
    try:
        logging.debug('opening postgres connection: %s:%s',
                      PGSQL_HOST, PGSQL_PORT)
        pgsql_conn = db.connect(host=PGSQL_HOST, port=int(
            PGSQL_PORT), user=PGSQL_USER, password=PGSQL_PASSWORD, dbname='ddstats')
        pgsql_conn.autocommit = True
        cursor: Cursor = pgsql_conn.cursor()
        yield cursor
    except DatabaseError as err:
        raise err
    finally:
        if cursor:
            cursor.close()
        if pgsql_conn:
            pgsql_conn.close()


@contextmanager
def select(stmt: str, args: tuple):
    with get_connection() as cursor:
        cursor.execute(stmt, args)
        yield cursor


def select_all(stmt: str, args: tuple):
    with select(stmt, args) as cursor:
        return cursor.fetchall()


def select_one(stmt: str, args: tuple):
    with select(stmt, args) as cursor:
        return cursor.fetchone()
