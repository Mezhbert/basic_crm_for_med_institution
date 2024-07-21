import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

# класс для работы с mysql с таблицей medical_records для истории жалоб
class ComplaintsHistory(metaclass=Singleton):
    def __init__(self, db, cursor):
        # сохраняем реквизиты бд
        self.m_db = db
        self.m_cursor = cursor

        # получаем путь до директории текущего скрипта
        parent_path = Path(__file__).parent

        # конкатенация путей и загрузка sql вызовов
        self.m_sql = Sql(os.path.join(parent_path, "sql/complaints_history.sql"))

    # взятие данных из таблицы
    def select(self) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("select")
            )

        # получаем результат
        return self.m_cursor.fetchall()

    def find_by_name_with_names(self, name : str):
        self.m_cursor.execute(
            self.m_sql.get_sql("find_by_name_with_names"),
            (name,)
            )

        # получаем результат
        return self.m_cursor.fetchall()
