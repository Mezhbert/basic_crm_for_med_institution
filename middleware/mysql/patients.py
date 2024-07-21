import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

import datetime

# класс для работы с mysql с таблицей пациентов
class Patients(metaclass=Singleton):
    def __init__(self, db, cursor):
        # сохраняем реквизиты бд
        self.m_db = db
        self.m_cursor = cursor

        # получаем путь до директории текущего скрипта
        parent_path = Path(__file__).parent

        # конкатенация путей и загрузка sql вызовов
        self.m_sql = Sql(os.path.join(parent_path, "sql/patients.sql"))

    # создание таблицы
    def create(self):
        try:
            self.m_cursor.execute(self.m_sql.get_sql("create"))

        except Exception as exc:
            pass

        # фиксация изменений
        self.m_db.commit()

    # вставка данных в таблицу
    def insert(self, name : str, birthdate : datetime, phone : str, gender : int, weight : float, height : float, disability : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("insert"),
            (name, birthdate, phone, gender, weight, height, disability)
            )

        # фимксация изменений
        self.m_db.commit()

    # обновление данных в таблице
    def update(self, id : int, name : str, birthdate : datetime, phone : str, gender : int, weight : float, height : float, disability : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("update"),
            (name, birthdate, phone, gender, weight, height, disability, id)
            )

        # фимксация изменений
        self.m_db.commit()

    # удаление данных из таблицы
    def delete(self, id : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("delete"), (id,)
            )

        # фимксация изменений
        self.m_db.commit()

    # взятие данных из таблицы
    def select(self) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("select_all")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # поиск данных по имени
    def find_by_name(self, name : str) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("find_by_name"),
            (name,)
            )

        # получаем результат
        return self.m_cursor.fetchall()

    def find_by_id(self, id : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("find_by_id"),
            (id,)
            )

        # получаем результат
        return self.m_cursor.fetchall()

    def find_by_name_picker(self, name : str) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("find_by_name_name_bd_phone"),
            (name,)
            )

        # получаем результат
        return self.m_cursor.fetchall()

    def select_picker(self) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("select_name_bd_phone")
            )

        # получаем результат
        return self.m_cursor.fetchall()
