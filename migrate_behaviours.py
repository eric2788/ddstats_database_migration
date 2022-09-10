import sys
from time import sleep
import pgsql
import mysql
from log import logger
from constrants import INSERT_RATE, MIN_BEHAVIOUR_ID, SLEEP


def create_pgsql_table():
    with pgsql.get_connection() as c:
        c.execute("""
            create table if not exists behaviours (
                id bigserial primary key,
                uid bigint not null,
                created_at timestamp not null,
                target_uid bigint not null,
                command varchar(255) not null,
                display text not null,
                image text default null,
                price double precision default 0,
                constraint behaviours_uid_fkey foreign key (uid) references vups (uid) on delete cascade,
                constraint behaviours_target_uid_fkey foreign key (target_uid) references vups (uid) on delete cascade
            );
        """)

def dump_database(values: list):
    logger.info("dumping to pgsql database...")
    with pgsql.get_connection() as cursor:
        cursor.executemany('insert into values (%s, %s, %s, %s, %s, %s, %s, %s) on conflict (id) do nothing', values)
    logger.info("successfully dumped.")


# huge data records so I can't select *
if __name__ == '__main__':

    sleep_time = float(SLEEP)
    interval = int(INSERT_RATE)
    min_id = int(MIN_BEHAVIOUR_ID)

    create_pgsql_table()
    logger.info("pgsql table created")
    logger.info('finding max id and min id...')
    result = mysql.select_one('select max(id) from behaviours')
    if not result:
        sys.exit(1)
    maxIdStr = result[0]
    max_id = int(maxIdStr)
    logger.info("max = %s, min = %s", max_id, min_id)
    values = []
    for i in range(min_id, max_id+1):
        if sleep_time > 0:
            sleep(sleep_time)
        row = mysql.select_one('select * from behaviours where id = %s', (i,))
        if not row:
            logger.warning("cannot find data with id %s, ignored.", i)
            continue
        values.append(row)
        if len(values) >= interval:
            logger.info('ready to dump %d records (to %d)', len(values), i)
            dump_database(values)
            logger.info('successfully dumped.')
            values = []