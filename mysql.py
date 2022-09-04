from constrants import *
import MySQLdb as db
from MySQLdb import Connection
from MySQLdb.cursors import Cursor
from MySQLdb._exceptions import DatabaseError
from contextlib import contextmanager
import logging

@contextmanager
def get_connection():
    try:
        logging.debug('opening mysql connection: %s', MYSQL_HOST)
        connection: Connection = db.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db='ddstats', charset='utf8')
        connection.autocommit(True)
        cursor: Cursor = connection.cursor()
        yield cursor
    except DatabaseError as error:
        logging.error(error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

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