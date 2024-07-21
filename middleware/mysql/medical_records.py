import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

import datetime

# класс для работы с mysql с таблицей медицинских карт
class MedicalRecords(metaclass=Singleton):
    def __init__(self, db, cursor):
        # сохраняем реквизиты бд
        self.m_db = db
        self.m_cursor = cursor

        # получаем путь до директории текущего скрипта
        parent_path = Path(__file__).parent

        # конкатенация путей и загрузка sql вызовов
        self.m_sql = Sql(os.path.join(parent_path, "sql/medical_records.sql"))

    # создание таблицы
    def create(self):
        try:
            self.m_cursor.execute(self.m_sql.get_sql("create"))

        except Exception as exc:
            pass

        # фиксация изменений
        self.m_db.commit()

    # вставка данных в таблицу
    def insert(self, id_patient : int, date : datetime, complaints : str, diagnosis : str, allergy : str, treatment : str, id_medication : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("insert"),
            (id_patient, date, complaints, diagnosis, allergy, treatment, id_medication)
            )

        # фиксация изменений
        self.m_db.commit()

    # обновление данных в таблице
    def update(self, id : int, id_patient : int, date : datetime, complaints : str, diagnosis : str, allergy : str, treatment : str, id_medication : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("update"),
            (id_patient, date, complaints, diagnosis, allergy, treatment, id_medication, id)
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

    # поиск по id пациента
    def find_by_patient_id(self, patient_id : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("find_by_patient_id"),
            (patient_id,)
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # поиск по id препарата
    def find_by_medication_id(self, medication_id : int):
        self.m_cursor.execute(
            self.m_sql.get_sql("find_by_medication_id"),
            (medication_id,)
            )

        # получаем результат
        return self.m_cursor.fetchall()

    # поиск записей по имени пациента
    def find_by_name_with_names(self, name : str):
        self.m_cursor.execute(
            self.m_sql.get_sql("find_by_name_with_names"),
            (name,)
            )

        # получаем результат
        return self.m_cursor.fetchall()
