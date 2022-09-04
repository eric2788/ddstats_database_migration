import pgsql, mysql


def create_pgsql_table():
    with pgsql.get_connection() as cursor:
        cursor.execute("""
            create table if not exists last_listens (
                uid bigint not null primary key,
                last_listen_at timestamp,
                constraint last_listens_uid_fkey foreign key (uid) references vups (uid) on delete cascade
            );
        """)


if __name__ == '__main__':
    pass