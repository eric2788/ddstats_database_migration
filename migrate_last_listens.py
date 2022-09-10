import sys
import pgsql
import mysql
from log import logger

def create_pgsql_table():
    with pgsql.get_connection() as cs:
        cs.execute("""
            create table if not exists last_listens (
                uid bigint not null primary key,
                last_listen_at timestamp,
                constraint last_listens_uid_fkey foreign key (uid) references vups (uid) on delete cascade
            );
        """)


if __name__ == '__main__':
    create_pgsql_table()
    logger.info("pgsql table created.")
    logger.info("searching all last_listens...")
    rows = mysql.select_all('select * from last_listens')
    if not rows:
        sys.exit(1)
    values = []
    for row in rows:
        values.append(row)
    with pgsql.get_connection() as cursor:
        cursor.executemany('insert into last_listens values (%s, %s) on conflict(uid) do nothing', values)
    logger.info("data inserted.")