import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

import datetime

# класс для работы с mysql с таблицей записей
class Appointments(metaclass=Singleton):
    def __init__(self, db, cursor):
        # сохраняем реквизиты бд
        self.m_db = db
        self.m_cursor = cursor

        # получаем путь до директории текущего скрипта
        parent_path = Path(__file__).parent

        # конкатенация путей и загрузка sql вызовов
        self.m_sql = Sql(os.path.join(parent_path, "sql/appointments.sql"))

    # создание таблицы
    def create(self):
        try:
            self.m_cursor.execute(self.m_sql.get_sql("create"))

        except Exception as exc:
            pass

        # фиксация изменений
        self.m_db.commit()

    # вставка данных в таблицу
    def insert(self, id_doctor : int, id_patient : int, date : datetime):
        self.m_cursor.execute(
            self.m_sql.get_sql("insert"),
            (id_doctor, id_patient, date)
            )

        # фимксация изменений
        self.m_db.commit()

    # обновление данных в таблице
    def update(self, id : int, id_doctor : int, id_patient : int, date : datetime):
        self.m_cursor.execute(
            self.m_sql.get_sql("update"),
            (id_doctor, id_patient, date, id)
            )

        # фимксация изменений
        self.m_db.commit()

    # удаление данных из таблицы
    def delete(self, id):
        self.m_cursor.execute(
            self.m_sql.get_sql("delete"), (id,)
            )

        # фимксация изменений
        self.m_db.commit()

    # взятие данных из таблицы
    def select(self) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("select_with_names")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # поиск данных по имени
    def find_by_names(self, doctor : str, patient : str) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("select_with_names_find_by_name"),
            (doctor, patient)
            )

        # получаем результат
        return self.m_cursor.fetchall()
