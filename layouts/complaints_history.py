import PySimpleGUI as sg
import operator
import mysql

from middleware.mysql import db

# ------ Complaints history Layout ------
class ComplaintsHistoryLayout:


    def __init__(self):
        self.m_window = None

        # последняя выделенная ячейка таблицы
        self.__selected_cell = (0, 0)

        # номер столбца по которому сортируется таблица
        self.__order_by = 0

        # данные таблицы
        self.__data = []

        # создаем window и храним его в self.m_window
        self.window()




    # создаем window и храним его в self.m_window
    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        # получение всех данных из бд
        self.__data = db.complaints_history.select()

        # описание окна со списком диагнозов
        complaints_history_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/Complaints history",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_COMPLAINTS_HISTORY_BACK-",
                    expand_x=True,
                    expand_y=False,
                    enable_events=True
                )
            ],
            [
                sg.Text(
                    text="Patient: ",
                    size=(5,)
                ),
                sg.Input(
                    key="-INPUT_COMPLAINTS_HISTORY_FIND_BY_NAME-",
                    enable_events=True,
                    expand_x=True
                )
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Id", "Patient", "Complaints", "Date of complaints"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=5,
                    key="-TABLE_COMPLAINTS_HISTORY-",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True
                )
            ]
        ]

        # создание window
        self.m_window = sg.Window("Complaints history", complaints_history_layout, resizable=True, finalize=True)

        return self.m_window


    

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
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_COMPLAINTS_HISTORY_BACK-":
            self.m_window.close()
            # отправляем команду
            args = (None,)
            return ("menu", args)

        # вводим поиск
        elif event == "-INPUT_COMPLAINTS_HISTORY_FIND_BY_NAME-":
            name = self.m_window["-INPUT_COMPLAINTS_HISTORY_FIND_BY_NAME-"].get()

            length = len(name)

            # поиск по первой букве
            if length == 1:
                # взятие данных из бд
                self.__data = db.complaints_history.find_by_name_with_names("{}%".format(name))

            # поиск по всему полю
            elif length > 1:
                # взятие данных из бд
                self.__data = db.complaints_history.find_by_name_with_names("%{}%".format(name))

            # ничего не ищем
            else:
                # взятие данных из бд
                self.__data = db.complaints_history.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_COMPLAINTS_HISTORY-"].update(self.__data)

        # если клик по таблице
        elif event[0] == "-TABLE_COMPLAINTS_HISTORY-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # если клик по заголовку таблицы
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_COMPLAINTS_HISTORY-"].update(self.__data)

        args = (None,)
        return (None, args)
