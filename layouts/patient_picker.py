import PySimpleGUI as sg
import operator
import mysql

from middleware.mysql import db

# ------ Patient_picker Layout ------
class PatientPickerLayout:


    def __init__(self, parent_layout : str):
        self.m_parent_layout = parent_layout

        self.m_window = None

        # номер столбца по которому сортируется таблица
        self.__order_by = 0

        # пустое имя
        self.m_name = ""

        # создаем window и храним его в self.m_window
        self.window()




    # создаем window и храним его в self.m_window
    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        # получение всех данных из бд
        self.__data = db.patient.select_picker()

        # описание окна с информацией о пациенте
        patient_picker_layout = [
            [
                [
                    sg.Text(
                        text="Patient:",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENT_PICKER_FIND_BY_NAME-",
                        enable_events=True,
                        expand_x=True
                    )
                ],
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Name", "Birthdate", "Phone"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=5,
                    key="-TABLE_PATIENT_PICKER-",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True
                )
            ],
            [
                sg.Button(
                    button_text="OK",
                    key="-BUTTON_PATIENT_PICKER_OK-",
                    enable_events=True,
                    expand_x=True
                )
            ]
        ]

        # создание window
        self.m_window = sg.Window("Patient picker", patient_picker_layout, resizable=True, finalize=True)

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
        if event == sg.WIN_CLOSED or event == "Cancel":
            self.m_window.close()

        # ввод имени в поисковик
        elif event == "-INPUT_PATIENT_PICKER_FIND_BY_NAME-":
            name = self.m_window["-INPUT_PATIENT_PICKER_FIND_BY_NAME-"].get()

            length = len(name)

            # поиск по первой букве
            if length == 1:
                # взятие данных из бд
                self.__data = db.patient.find_by_name_picker("{}%".format(name))

            # поиск по всему полю
            elif length > 1:
                # взятие данных из бд
                self.__data = db.patient.find_by_name_picker("%{}%".format(name))

            # ничего не ищем
            else:
                # взятие данных из бд
                self.__data = db.patient.select_picker()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_PATIENT_PICKER-"].update(self.__data)

        # если клик по таблице
        elif event[0] == "-TABLE_PATIENT_PICKER-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # если клик по заголовку таблицы
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_PATIENT_PICKER-"].update(self.__data)

            # если клик не по ячейке или заголовку таблицы
            elif row is None or col is None:
                self.__selected_cell = None

                # сброс сохраненного имени
                self.m_name = ""

                # снятие выделения
                self.m_window["-TABLE_PATIENT_PICKER-"].update(select_rows=[])

            # если клик по ячейке
            else:
                # сохранение имени из выделенной строки
                self.m_name = self.__data[self.__selected_cell[0]][0]

        # если клик по кнопке ok
        elif event == "-BUTTON_PATIENT_PICKER_OK-":
            self.m_window.close()
            args = (self.m_name, self.m_parent_layout)
            return ("picked_patient", args)

        args = (None,)
        return (None, args)
