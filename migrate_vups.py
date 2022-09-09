import sys
from log import logger as logging
import pgsql
import mysql


def create_pgsql_table():
    with pgsql.get_connection() as cur:
        cur.execute("""
            create table if not exists vups (
                uid bigint not null primary key,
                name varchar(200) not null,
                face text not null,
                first_listen_at timestamp not null,
                room_id bigint not null,
                sign varchar(255) default ''::character varying
            );
        """)


if __name__ == '__main__':
    create_pgsql_table()
    logging.info("pgsql table created")
    logging.info('searching all vups from mysql...')
    results = mysql.select_all('select * from vups')
    if not results:
        sys.exit(1)
    values = []
    logging.info('searched %d vups from mysql.', len(results))
    for row in results:
        values.append(row)
    with pgsql.get_connection() as cursor:
        a = cursor.executemany(
            'insert into vups values (%s, %s, %s, %s, %s, %s) on conflict (uid) do nothing', values)
    logging.info("data inserted")
