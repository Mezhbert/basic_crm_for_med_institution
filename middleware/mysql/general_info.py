import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

# класс для работы с mysql с разных для общей информации
class GeneralInfo(metaclass=Singleton):
    def __init__(self, db, cursor):
        # сохраняем реквизиты бд
        self.m_db = db
        self.m_cursor = cursor

        # получаем путь до директории текущего скрипта
        parent_path = Path(__file__).parent

        # конкатенация путей и загрузка sql вызовов
        self.m_sql = Sql(os.path.join(parent_path, "sql/general_info.sql"))

    # взятие данных из таблицы
    def select(self) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("select")
            )

        # получаем результат
        return self.m_cursor.fetchall()


    # взятие данных из таблицы
    def count_doctors(self):
        self.m_cursor.execute(
            self.m_sql.get_sql("count_doctors")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # взятие данных из таблицы
    def count_patients(self):
        self.m_cursor.execute(
            self.m_sql.get_sql("count_patients")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # взятие данных из таблицы
    def count_patients_without_disablity(self):
        self.m_cursor.execute(
            self.m_sql.get_sql("count_patients_without_disablity")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # взятие данных из таблицы
    def count_patients_with_1_disablity(self):
        self.m_cursor.execute(
            self.m_sql.get_sql("count_patients_with_1_disablity")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # взятие данных из таблицы
    def count_patients_with_2_disablity(self):
        self.m_cursor.execute(
            self.m_sql.get_sql("count_patients_with_2_disablity")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # взятие данных из таблицы
    def count_patients_with_3_disablity(self):
        self.m_cursor.execute(
            self.m_sql.get_sql("count_patients_with_3_disablity")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # взятие данных из таблицы
    def count_patients_with_4_disablity(self):
        self.m_cursor.execute(
            self.m_sql.get_sql("count_patients_with_4_disablity")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # взятие данных из таблицы
    def count_medications(self):
        self.m_cursor.execute(
            self.m_sql.get_sql("count_medications")
        )

        # получаем результат
        return self.m_cursor.fetchall()
