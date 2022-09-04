import pgsql, mysql

def create_pgsql_table():
    with pgsql.get_connection() as cursor:
        cursor.execute("""
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
    pass

