# класс пустышка
# объект этого класса можно передавать в Doctors, Patients и тд вместо реального объекта бд
class DbPlaceholder:
    def commit(self):
        pass
