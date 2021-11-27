import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from Admin_panel_sprint_1.sqlite_to_postgres.sqlite_loader import SQLiteLoader
from Admin_panel_sprint_1.sqlite_to_postgres.postres_saver import PostgresSaver
from conf import dsl
from log_config import *


@logger.catch
def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()

    pg_conn.close()
