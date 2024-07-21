import os

from pathlib import Path

from singleton import Singleton

from .sql import Sql

# класс для работы с mysql с таблицей типов инвалидности
class DisabilityType(metaclass=Singleton):
    def __init__(self, db, cursor):
        # сохраняем реквизиты бд
        self.m_db = db
        self.m_cursor = cursor

        # получаем путь до директории текущего скрипта
        parent_path = Path(__file__).parent

        # конкатенация путей и загрузка sql вызовов
        self.m_sql = Sql(os.path.join(parent_path, "sql/disability_types.sql"))

    # создание таблицы
    def create(self):
        try:
            self.m_cursor.execute(self.m_sql.get_sql("create"))

        except Exception as exc:
            pass

        # фиксация изменений
        self.m_db.commit()

    # вставка данных в таблицу
    def insert(self, type : str):
        try:
            self.m_cursor.execute(
                self.m_sql.get_sql("insert"),
                (type,)
                )
        except Exception as exc:
            pass

        # фимксация изменений
        self.m_db.commit()

    # взятие данных из таблицы
    def select(self) -> tuple:
        self.m_cursor.execute(
            self.m_sql.get_sql("select")
            )

        # получаем результат
        return self.m_cursor.fetchall()
