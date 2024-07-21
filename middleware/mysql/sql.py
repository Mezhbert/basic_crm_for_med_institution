# класс для чтения .sql файлов
class Sql:
    def __init__(self, sql_path):
        self.__m_sql = self.__load(sql_path)

    # чтение данных из файла
    def __load(self, sql_path) -> list:

        # чтение файла целиком
        def full_read(sql_path) -> str:
            with open(sql_path, 'r') as f:
                return f.read()

        sql_file = full_read(sql_path)

        # разделяем содержимое .sql файла на отдельные вызовы
        sql_dict = dict()
        for command in sql_file.split(';'):
            key = ""
            value = ""

            if len(command) < 2:
                continue

            # поиск id и соответствующей команды
            for line in command.split('\n'):

                if line.startswith("#"):
                    key = line[1:]

                else:
                    value += line + '\n'

            # не найден id
            if not key:
                print("key not found at '{0}' sql command".format(value))
                continue

            sql_dict.update({key: value})

        ## избавляемся от символов пробела, табулции и перевода строки
        #sql = list(map(lambda x: x.strip(" \t\n"), sql))

        return sql_dict

    # возвращает текст вызова по префиксу
    def get_sql(self, id : str) -> str:
        return self.__m_sql.get(id)
