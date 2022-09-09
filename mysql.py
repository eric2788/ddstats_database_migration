from contextlib import contextmanager
import MySQLdb as db
from MySQLdb import Connection
from MySQLdb.cursors import Cursor
from MySQLdb._exceptions import DatabaseError
from log import logger as logging
from constrants import *


@contextmanager
def get_connection():
    cursor = None
    connection = None
    try:
        logging.debug('opening mysql connection: %s:%s',
                      MYSQL_HOST, MYSQL_PORT)
        connection: Connection = db.connect(host=MYSQL_HOST, port=int(
            MYSQL_PORT), user=MYSQL_USER, passwd=MYSQL_PASSWORD, db='ddstats', charset='utf8')
        connection.autocommit(True)
        cursor: Cursor = connection.cursor()
        yield cursor
    except DatabaseError as error:
        raise error
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@contextmanager
def select(stmt: str, args: tuple = ()):
    with get_connection() as cursor:
        cursor.execute(stmt, args)
        yield cursor


def select_all(stmt: str, args: tuple = ()):
    try:
        with select(stmt, args) as cursor:
            return cursor.fetchall()
    except DatabaseError as err:
        logging.error(err)
        return None


def select_one(stmt: str, args: tuple = ()):
    try:
        with select(stmt, args) as cursor:
            return cursor.fetchone()
    except DatabaseError as err:
        logging.error(err)
        return None
