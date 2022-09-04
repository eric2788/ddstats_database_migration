import pgsql, mysql


def create_pgsql_table():
    with pgsql.get_connection() as cursor:
        cursor.execute("""
            create table if not exists behaviours (
                id serial primary key,
                uid bigint not null,
                created_at timestamp not null,
                target_uid bigint not null,
                command varchar(255) not null,
                display text not null,
                image text default null,
                price double precision default 0,
                constraint behaviours_uid_fkey foreign key (uid) references vups (uid) on delete cascade
                constraints behaviours_target_uid_fkey foreign key (target_uid) references vups (uid) on delete cascade
            );
        """)



if __name__ == '__main__':
    pass