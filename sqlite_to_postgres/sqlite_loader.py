import sqlite3

from typing import List, Dict

from schemas import (
        FilmWorkWithoutField, GenreWithoutField, GenreFilmWorkWithoutField,
        PersonWithoutField, PersonFilmWithoutField
    )


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection, schemas: dict = None):
        self.__connection = connection
        self.__connection.row_factory = sqlite3.Row
        self.__cursor = self.__connection.cursor()
        self.__schemas = schemas
        self.__initialize_schemas()

    def __initialize_schemas(self):
        if self.__schemas is None:
            self.__schemas = {
                'film_work': FilmWorkWithoutField,
                'genre': GenreWithoutField,
                'person': PersonWithoutField,
                'genre_film_work': GenreFilmWorkWithoutField,
                'person_film_work': PersonFilmWithoutField
            }

    @staticmethod
    def __get_schema_keys(schema) -> List[str]:
        return list(schema.__dict__.get('__annotations__').keys())

    def __load_table(self, schema: type, table_name: str) -> List[type]:
        data = []
        keys = self.__get_schema_keys(schema)
        rows = self.__cursor.execute(f'SELECT * FROM {table_name}')
        for row in rows:
            data_row = {key: row[key] for key in keys}
            data.append(schema(**data_row))
        return data

    def load_movies(self) -> Dict[str, list]:
        return {table_name: self.__load_table(schema, table_name) for table_name, schema in self.__schemas.items()}
