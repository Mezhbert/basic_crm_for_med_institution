import PySimpleGUI as sg
import operator
import mysql

from middleware.mysql import db

# ------ Medications Layout ------
class MedicationsLayout:


    def __init__(self):
        # последняя выделенная ячейка таблицы
        self.__selected_cell = (0, 0)

        # номер столбца по которому сортируется таблица
        self.__order_by = 0

        # данные таблицы
        self.__data = []

        self.m_window = None

        # создаем window и храним его в self.m_window
        self.window()




    # создаем window и храним его в self.m_window
    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        # получение всех данных из бд
        self.__data = db.medication.select()

        # описание окна с таблицей карт
        medications_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/Medications",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_MEDICATIONS_BACK-",
                    expand_x=True,
                    expand_y=False,
                    enable_events=True
                )
            ],
            [
                sg.Text(
                    text="Medication: ",
                    size=(5,)
                ),
                sg.Input(
                    key="-INPUT_MEDICATIONS_FIND_BY_NAME-",
                    enable_events=True,
                    expand_x=True
                )
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Id", "Title", "Desc", "Contraindication"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=5,
                    key="-TABLE_MEDICATIONS-",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True
                )
            ],
            [
                [
                    sg.Text(
                        text="Title",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_MEDICATIONS_TITLE-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Desc",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_MEDICATIONS_DESC-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Contraindication",
                        size=(10,)
                    ),
                    sg.Input(
                        key="-INPUT_MEDICATIONS_CONTRAINDICATION-",
                        expand_x=True
                    )
                ],
                [
                    sg.Button(
                        button_text="Insert",
                        key="-BUTTON_MEDICATIONS_INSERT-",
                        enable_events=True
                    ),
                    sg.Button(
                        button_text="Update",
                        key="-BUTTON_MEDICATIONS_UPDATE-",
                        enable_events=True,
                        disabled=True
                    ),
                    sg.Button(
                        button_text="Delete",
                        key="-BUTTON_MEDICATIONS_DELETE-",
                        enable_events=True,
                        disabled=True
                    )
                ]
            ]
        ]

        # создание window
        self.m_window = sg.Window("Medications", medications_layout, resizable=True, finalize=True)

        return self.m_window




    # сбор данных с формы
    def __get_record_form(self) -> tuple:
        return (
            self.m_window["-INPUT_MEDICATIONS_TITLE-"].get(),
            self.m_window["-INPUT_MEDICATIONS_DESC-"].get(),
            self.m_window["-INPUT_MEDICATIONS_CONTRAINDICATION-"].get()
        )




    # запись данных в форму
    def __set_record_form(self, title : str, desc : str, contraindication : str):
        self.m_window["-INPUT_MEDICATIONS_TITLE-"].update(value=title),
        self.m_window["-INPUT_MEDICATIONS_DESC-"].update(value=desc),
        self.m_window["-INPUT_MEDICATIONS_CONTRAINDICATION-"].update(value=contraindication)




    """ sort a table by multiple columns
    table: a list of lists (or tuple of tuples) where each inner list
            represents a row
    cols:  a list (or tuple) specifying the column numbers to sort by
            e.g. (1,0) would sort by column 1, then by column 0
    """
    def __sort_table(self, cols):
        for col in reversed(cols):
            try:
                self.__data = sorted(self.__data, key=operator.itemgetter(col))
            except Exception as e:
                sg.popup_error("Error in sort_table", "Exception in sort_table", e)




    # обработчик событий приложения
    def events_handler(self, event, values):
        # если клик по кнопке назад или закрытие окна
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_MEDICATIONS_BACK-":
            self.m_window.close()
            # отправляем команду
            args = (None,)
            return ("menu", args)

        elif event == "-INPUT_MEDICATIONS_FIND_BY_NAME-":
            name = self.m_window["-INPUT_MEDICATIONS_FIND_BY_NAME-"].get()

            length = len(name)

            # поиск по первой букве
            if length == 1:
                # взятие данных из бд
                self.__data = db.medication.find_by_name("{}%".format(name))

            # поиск по всему полю
            elif length > 1:
                # взятие данных из бд
                self.__data = db.medication.find_by_name("%{}%".format(name))

            # ничего не ищем
            else:
                # взятие данных из бд
                self.__data = db.medication.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_MEDICATIONS-"].update(self.__data)

        # если клик по таблице
        elif event[0] == "-TABLE_MEDICATIONS-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # если клик по заголовку таблицы
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_MEDICATIONS-"].update(self.__data)

            # если клик не по ячейке или заголовку таблицы
            elif row is None or col is None:
                self.__selected_cell = None

                # сброс данных в форме
                self.__set_record_form(*("", "", ""))

                # снятие выделения
                self.m_window["-TABLE_MEDICATIONS-"].update(select_rows=[])
                
                # отключение кнопок
                self.m_window["-BUTTON_MEDICATIONS_UPDATE-"].update(disabled=True)
                self.m_window["-BUTTON_MEDICATIONS_DELETE-"].update(disabled=True)

            # если клик по ячейке
            else:
                # взятие данных из выделенной строки
                old_record = self.__data[self.__selected_cell[0]]

                # заполнение формы данными
                self.__set_record_form(*old_record[1:])

                # включение кнопок
                self.m_window["-BUTTON_MEDICATIONS_UPDATE-"].update(disabled=False)
                self.m_window["-BUTTON_MEDICATIONS_DELETE-"].update(disabled=False)

        # если клик по кнопке вставить
        elif event == "-BUTTON_MEDICATIONS_INSERT-":
            # взятие данных с формы
            try:
                new_record = list(self.__get_record_form())

            except Exception as err:
                # обработка исключения
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                args = (None,)
                return (None, args)

            # попытка отправить данные в бд
            try:
                db.medication.insert(*new_record)

            except mysql.connector.IntegrityError as err:
                # обработка исключения
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                args = (None,)
                return (None, args)

            # взятие данных их бд
            self.__data = db.medication.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_MEDICATIONS-"].update(self.__data)

        # если клик по кнопке обновить
        elif event == "-BUTTON_MEDICATIONS_UPDATE-":
            if not self.__selected_cell:
                args = (None,)
                return (None, args)

            row, col = self.__selected_cell

            # берем данные выделенной строки
            old_record = self.__data[row]

            # на ее основе формируем данные для отправки
            new_record = list((old_record[0],) + self.__get_record_form())

            # попытка отправить данные в бд
            try:
                db.medication.update(*new_record)

            except mysql.connector.IntegrityError as err:
                # обработка исключения
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                args = (None,)
                return (None, args)

            # обновление перезаписанных данных в строке
            self.__data[row] = new_record

            # взятие данных из бд
            self.__data = db.medication.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_MEDICATIONS-"].update(self.__data)

        # если клик по кнопке удалить
        elif event == "-BUTTON_MEDICATIONS_DELETE-":
            if not self.__selected_cell:
                args = (None,)
                return (None, args)

            row, col = self.__selected_cell

            # берем данные выделенной строки
            old_record = self.__data[row]

            # попытка удалить данные из бд
            db.medication.delete(old_record[0])
            
            # check results ???

            # удаление данных
            self.__data.remove(old_record)

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_MEDICATIONS-"].update(self.__data)

        args = (None,)
        return (None, args)
