# класс упрощающий хранить данные и формировать нужные данные в combo элемент
class ComboListData:
    def __init__(self, rules : dict = {}, data : list = []):
        self.load_data(rules, data)

    # загрузка данных в класс
    def load_data(self, rules : dict, data : list):
        self.__data = list()

        # процесс фильтрации данных
        for e in data:
            ins = dict()
            
            # подготовка к добавлению данных
            for idx, col in rules.items():
                ins[col] = e[idx]

            # добавление данных
            self.__data.append(ins)

        # отсутствие запеченных данных
        self.__precoockedData = None

    # returns get_value
    def get_column(self, get_column : str, find_column : str, find_value : str):
        for e in self.__data:
            if e.get(find_column) == find_value:
                return e.get(get_column)

        return None

    # запечка данных для сокращения обработки данных
    def __coocking_data(self, columns : list):
        return list(map(lambda x : " ".join([x.get(c) for c in columns]), self.__data))

    # получение запеченных данных
    def get_combo_data(self, columns : list):
        # если запеченных данных нет
        if not self.__precoockedData:
            # запекаем
            self.__precoockedData = self.__coocking_data(columns)

        return self.__precoockedData

    # получение данных по умолчанию
    def get_default_value(self) -> str:
        if self.__precoockedData:
            return self.get_combo_data([])[0]

        # ошибка, если данные не запечены, или в запечке учавствовал пустой список с данными
        return self.get_combo_data()[0]
