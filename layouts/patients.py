import PySimpleGUI as sg
import operator
import mysql

from middleware.mysql import db

from datetime import datetime

from .utils.combo_list_data import ComboListData

# ------ Patients Layout ------
class PatientsLayout:


    def __init__(self):
        # последняя выделенная ячейка таблицы
        self.__selected_cell = (0, 0)

        # номер столбца по которому сортируется таблица
        self.__order_by = 0

        # данные таблицы
        self.__data = []

        # список отображающийся в графе пол
        self.__comboGenderData = ComboListData()

        # список отображающийся в графе инвалидность
        self.__comboDisabilityData = ComboListData()

        self.m_window = None

        # создаем window и храним его в self.m_window
        self.window()




    # создаем window и храним его в self.m_window
    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        # получение всех данных из бд
        self.__data = db.patient.select()

        # получение данных о полах и инвалидности
        genders = db.gender_type.select()
        disabilities = db.disability_type.select()

        self.__comboGenderData.load_data({0 : "id", 1 : "type"}, genders)
        self.__comboDisabilityData.load_data({0 : "id", 1 : "type"}, disabilities)

        # описание окна с таблицей пациентов
        patients_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/Patients",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_PATIENTS_BACK-",
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
                    key="-INPUT_PATIENTS_FIND_BY_NAME-",
                    enable_events=True,
                    expand_x=True
                )
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Id", "Name", "Birthdate", "Phone", "Gender", "Weight", "Height", "Disability"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=5,
                    key="-TABLE_PATIENTS-",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True
                )
            ],
            [
                [
                    sg.Text(
                        text="Name",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_NAME-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Birthdate",
                        size=(7,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_BIRTHDATE-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Phone",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_PHONE-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Gender",
                        size=(5,)
                    ),
                    sg.Combo(
                        key="-COMBO_PATIENTS_GENDER-",
                        values=self.__comboGenderData.get_combo_data(["type"]),
                        default_value=self.__comboGenderData.get_default_value(),
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Weight",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_WEIGHT-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Height",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_HEIGHT-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Disability",
                        size=(7,)
                    ),
                    sg.Combo(
                        key="-COMBO_PATIENTS_DISABILITY-",
                        values=self.__comboDisabilityData.get_combo_data(["type"]),
                        default_value=self.__comboDisabilityData.get_default_value(),
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Button(
                        button_text="Insert",
                        key="-BUTTON_PATIENTS_INSERT-",
                        enable_events=True
                    ),
                    sg.Button(
                        button_text="Update",
                        key="-BUTTON_PATIENTS_UPDATE-",
                        enable_events=True,
                        disabled=True
                    ),
                    sg.Button(
                        button_text="Delete",
                        key="-BUTTON_PATIENTS_DELETE-",
                        enable_events=True,
                        disabled=True
                    )
                ]
            ]
        ]

        # создание window
        self.m_window = sg.Window("Patients", patients_layout, resizable=True, finalize=True)

        return self.m_window




    # сбор данных с формы
    def __get_record_form(self) -> tuple:
        return (
            self.m_window["-INPUT_PATIENTS_NAME-"].get(),
            datetime.strptime(self.m_window["-INPUT_PATIENTS_BIRTHDATE-"].get(), "%d.%m.%y"),
            self.m_window["-INPUT_PATIENTS_PHONE-"].get(),
            self.m_window["-COMBO_PATIENTS_GENDER-"].get(),
            self.m_window["-INPUT_PATIENTS_WEIGHT-"].get(),
            self.m_window["-INPUT_PATIENTS_HEIGHT-"].get(),
            self.m_window["-COMBO_PATIENTS_DISABILITY-"].get()
        )




    # запись данных в форму
    def __set_record_form(self, name : str, birthdate : datetime, phone : str, gender : int, weight : float, height : float, disability : int):
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d %H:%M:%S')
        self.m_window["-INPUT_PATIENTS_NAME-"].update(value=name),
        self.m_window["-INPUT_PATIENTS_BIRTHDATE-"].update(value=birthdate.strftime("%d.%m.%y")),
        self.m_window["-INPUT_PATIENTS_PHONE-"].update(value=phone)
        self.m_window["-COMBO_PATIENTS_GENDER-"].update(value=gender)
        self.m_window["-INPUT_PATIENTS_WEIGHT-"].update(value=weight)
        self.m_window["-INPUT_PATIENTS_HEIGHT-"].update(value=height)
        self.m_window["-COMBO_PATIENTS_DISABILITY-"].update(value=disability)




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
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_PATIENTS_BACK-":
            self.m_window.close()
            # отправляем команду
            args = (None,)
            return ("menu", args)

        # клик по поиску
        elif event == "-INPUT_PATIENTS_FIND_BY_NAME-":
            name = self.m_window["-INPUT_PATIENTS_FIND_BY_NAME-"].get()

            length = len(name)

            # поиск по первой букве
            if length == 1:
                # взятие данных из бд
                self.__data = db.patient.find_by_name("{}%".format(name))

            # поиск по всему полю
            elif length > 1:
                # взятие данных из бд
                self.__data = db.patient.find_by_name("%{}%".format(name))

            # ничего не ищем
            else:
                # взятие данных из бд
                self.__data = db.patient.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_PATIENTS-"].update(self.__data)


        # если клик по таблице
        elif event[0] == "-TABLE_PATIENTS-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # если клик по заголовку таблицы
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_PATIENTS-"].update(self.__data)

            # если клик не по ячейке или заголовку таблицы
            elif row is None or col is None:
                self.__selected_cell = None

                # сброс данных в форме
                self.__set_record_form(*("", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "", self.__comboGenderData.get_default_value(), 0, 0, self.__comboDisabilityData.get_default_value()))

                # снятие выделения
                self.m_window["-TABLE_PATIENTS-"].update(select_rows=[])

                # отключение кнопок
                self.m_window["-BUTTON_PATIENTS_UPDATE-"].update(disabled=True)
                self.m_window["-BUTTON_PATIENTS_DELETE-"].update(disabled=True)

            else:
                # взятие данных из выделенной строки
                old_record = self.__data[self.__selected_cell[0]]

                # заполнение формы данными
                self.__set_record_form(*old_record[1:])

                # включение кнопок
                self.m_window["-BUTTON_PATIENTS_UPDATE-"].update(disabled=False)
                self.m_window["-BUTTON_PATIENTS_DELETE-"].update(disabled=False)

        # если клик по кнопке вставить
        elif event == "-BUTTON_PATIENTS_INSERT-":
            # взятие данных с формы
            new_record = list(self.__get_record_form())

            # замена type пола на id
            new_record[3] = int(self.__comboGenderData.get_column("id", "type", new_record[3]))

            # замена type инвалидности на id
            new_record[6] = int(self.__comboDisabilityData.get_column("id", "type", new_record[6]))

            # попытка отправить данные в бд
            try:
                db.patient.insert(*new_record)

            except mysql.connector.IntegrityError as err:
                # обработка исключения
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                args = (None,)
                return (None, args)

            # взятие данных их бд
            self.__data = db.patient.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_PATIENTS-"].update(self.__data)

        # если клик по кнопке обновить
        elif event == "-BUTTON_PATIENTS_UPDATE-":
            if not self.__selected_cell:
                args = (None,)
                return (None, args)

            row, col = self.__selected_cell
            # берем данные выделенной строки
            old_record = self.__data[row]

            # на ее основе формируем данные для отправки
            new_record = list((old_record[0],) + self.__get_record_form())

            # замена type пола на id
            new_record[4] = int(self.__comboGenderData.get_column("id", "type", new_record[4]))

            # замена type инвалидности на id
            new_record[7] = int(self.__comboDisabilityData.get_column("id", "type", new_record[7]))

            # попытка отправить данные в бд
            try:
                db.patient.update(*new_record)

            except mysql.connector.IntegrityError as err:
                # обработка исключения
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                args = (None,)
                return (None, args)

            # обновление перезаписанных данных в строке
            self.__data[row] = new_record

            # взятие данных их бд
            self.__data = db.patient.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_PATIENTS-"].update(self.__data)

        # если клик по кнопке удалить
        elif event == "-BUTTON_PATIENTS_DELETE-":
            if not self.__selected_cell:
                args = (None,)
                return (None, args)

            row, col = self.__selected_cell

            # берем данные выделенной строки
            old_record = self.__data[row]

            # попытка удалить данные из бд
            db.patient.delete(old_record[0])
        
            # check results ???

            # удаление данных
            self.__data.remove(old_record)

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_PATIENTS-"].update(self.__data)

        args = (None,)
        return (None, args)
