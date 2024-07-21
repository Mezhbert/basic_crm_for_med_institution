import PySimpleGUI as sg
import operator
import mysql

from datetime import datetime

from middleware.mysql import db

from .utils.combo_list_data import ComboListData

# ------ Appointments Layout ------
class AppointmentsLayout:


    def __init__(self):
        # последняя выделенная ячейка таблицы
        self.__selected_cell = (0, 0)

        # номер столбца по которому сортируется таблица
        self.__order_by = 0

        # список отображающийся в графе врач
        self.__comboDoctorData = ComboListData()

        # список отображающийся в графе пациент
        self.__comboPatientData = ComboListData()

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
        self.__data = db.appointment.select()

        doctors = db.doctor.select()
        patients = db.patient.select()

        if not doctors:
            self.__comboDoctorData.load_data({0 : "id", 1 : "name"}, [[-1, "NO DOCTORS"]])

        else:
            self.__comboDoctorData.load_data({0 : "id", 1 : "name"}, doctors)

        if not patients:
            self.__comboPatientData.load_data({0 : "id", 1 : "name"}, [[-1, "NO PATIENTS"]])

        else:
            self.__comboPatientData.load_data({0 : "id", 1 : "name"}, patients)

        # описание окна с таблицей записей
        appointments_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/Appointments",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_APPOINTMENTS_BACK-",
                    expand_x=True,
                    expand_y=False,
                    enable_events=True
                )
            ],
            [
                sg.Text(
                    text="Doctor: ",
                    size=(5,)
                ),
                sg.Input(
                    key="-INPUT_APPOINTMENTS_FIND_BY_DOCTORS_NAME-",
                    enable_events=True,
                    expand_x=True
                )
            ],
            [
                sg.Text(
                    text="Patient: ",
                    size=(5,)
                ),
                sg.Input(
                    key="-INPUT_APPOINTMENTS_FIND_BY_PATIENTS_NAME-",
                    enable_events=True,
                    expand_x=True
                )
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Id", "Doctor", "Birthdate", "Patient", "Birthdate", "Date"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=5,
                    key="-TABLE_APPOINTMENTS-",
                    selected_row_colors="red on yellow",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True
                )
            ],
            [
                [
                    sg.Text(
                        text="Doctor",
                        size=(7,)
                    ),
                    sg.Combo(
                        key="-COMBO_APPOINTMENTS_DOCTORS-",
                        values=self.__comboDoctorData.get_combo_data(["name"]),
                        default_value=self.__comboDoctorData.get_default_value(),
                        readonly=True,
                        expand_x=True
                    ),
                    sg.Button(
                        button_text="Find",
                        key="-BUTTON_APPOINTMENTS_DOCTOR_PICKER-",
                        enable_events=True
                    )
                ],
                [
                    sg.Text(
                        text="Patient",
                        size=(7,)
                    ),
                    sg.Combo(
                        key="-COMBO_APPOINTMENTS_PATIENTS-",
                        values=self.__comboPatientData.get_combo_data(["name"]),
                        default_value=self.__comboPatientData.get_default_value(),
                        readonly=True,
                        expand_x=True
                    ),
                    sg.Button(
                        button_text="Find",
                        key="-BUTTON_APPOINTMENTS_PATIENT_PICKER-",
                        enable_events=True
                    )
                ],
                [
                    sg.Text(
                        text="Date",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_APPOINTMENTS_DATE-",
                        expand_x=True
                    )
                ],
                [
                    sg.Button(
                        button_text="Insert",
                        key="-BUTTON_APPOINTMENTS_INSERT-",
                        enable_events=True
                    ),
                    sg.Button(
                        button_text="Update",
                        key="-BUTTON_APPOINTMENTS_UPDATE-",
                        enable_events=True,
                        disabled=True
                    ),
                    sg.Button(
                        button_text="Delete",
                        key="-BUTTON_APPOINTMENTS_DELETE-",
                        enable_events=True,
                        disabled=True
                    )
                ]
            ]
        ]

        # создание window
        self.m_window = sg.Window("Appointments", appointments_layout, resizable=True, finalize=True)

        # если нет хотя бы одного врача и пациента
        if not doctors and not patients:
            info_message = "There is no any doctors or patients"

        elif not doctors:
            info_message = "There is no any doctors"

        elif not patients:
            info_message = "There is no any patients"

        else:
            return self.m_window

        sg.popup_ok("Warning", info_message)
        self.m_window["-BUTTON_APPOINTMENTS_INSERT-"].update(disabled=True)

        return self.m_window




    # сбор данных с формы
    def __get_record_form(self) -> tuple:
        return (
            #self.__comboDoctorData.get_column("id", "name", self.m_window["-COMBO_APPOINTMENTS_DOCTORS-"].get()),
            #self.__comboPatientData.get_column("id", "name", self.m_window["-COMBO_APPOINTMENTS_PATIENTS-"].get()),
            self.m_window["-COMBO_APPOINTMENTS_DOCTORS-"].get(),
            self.m_window["-COMBO_APPOINTMENTS_PATIENTS-"].get(),
            datetime.strptime(self.m_window["-INPUT_APPOINTMENTS_DATE-"].get(), "%Y.%m.%d %H:%M:%S")
        )




    # запись данных в форму
    def __set_record_form(self, id_doctors : int, id_patients : int, date : datetime):
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        #self.m_window["-COMBO_APPOINTMENTS_DOCTORS-"].update(value=self.__comboDoctorData.get_column("name", "id", id_doctors)),
        #self.m_window["-COMBO_APPOINTMENTS_PATIENTS-"].update(value=self.__comboPatientData.get_column("name", "id", id_patients)),
        self.m_window["-COMBO_APPOINTMENTS_DOCTORS-"].update(value=id_doctors),
        self.m_window["-COMBO_APPOINTMENTS_PATIENTS-"].update(value=id_patients),
        self.m_window["-INPUT_APPOINTMENTS_DATE-"].update(value=date.strftime("%Y.%m.%d %H:%M:%S"))




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





    def set_doctor_name(self, name : str):
        if not name:
            name = self.__comboDoctorData.get_default_value()

        self.m_window["-COMBO_APPOINTMENTS_DOCTORS-"].update(value=name)

    def set_patient_name(self, name : str):
        if not name:
            name = self.__comboPatientData.get_default_value()

        self.m_window["-COMBO_APPOINTMENTS_PATIENTS-"].update(value=name)

    # обработчик событий приложения
    def events_handler(self, event, values):
        # если клик по кнопке назад или закрытие окна
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_APPOINTMENTS_BACK-":
            self.m_window.close()
            # отправляем команду
            args = (None,)
            return ("menu", args)

        elif event == "-BUTTON_APPOINTMENTS_DOCTOR_PICKER-":
            args = (None,)

            # открытие окна просмотрщика докторов
            return ("doctor_picker", args)

        elif event == "-BUTTON_APPOINTMENTS_PATIENT_PICKER-":
            args = (None,)

            # открытие окна просмотрщика пациентов
            return ("patient_picker", args)

        elif event == "-INPUT_APPOINTMENTS_FIND_BY_DOCTORS_NAME-" or event == "-INPUT_APPOINTMENTS_FIND_BY_PATIENTS_NAME-":
            doctor = self.m_window["-INPUT_APPOINTMENTS_FIND_BY_DOCTORS_NAME-"].get()
            patient = self.m_window["-INPUT_APPOINTMENTS_FIND_BY_PATIENTS_NAME-"].get()

            length = len(doctor)

            # поиск по первой букве
            if length == 1:
                doctor = "{}%".format(doctor)

            # поиск по всему полю
            elif length > 1:
                doctor = "%{}%".format(doctor)

            # ничего не ищем
            else:
                doctor = "%"

            # повторяем для пациента
            length = len(patient)

            # поиск по первой букве
            if length == 1:
                patient = "{}%".format(patient)

            # поиск по всему полю
            elif length > 1:
                patient = "%{}%".format(patient)

            # ничего не ищем
            else:
                patient = "%"

            # взятие данных из бд
            self.__data = db.appointment.find_by_names(doctor, patient)

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)

        # если клик по таблице
        elif event[0] == "-TABLE_APPOINTMENTS-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # если клик по заголовку таблицы
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)

            # если клик не по ячейке или заголовку таблицы
            elif row is None or col is None:
                self.__selected_cell = None

                # сброс данных в форме
                self.__set_record_form(*(self.__comboDoctorData.get_default_value(), self.__comboPatientData.get_default_value(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                # снятие выделения
                self.m_window["-TABLE_APPOINTMENTS-"].update(select_rows=[])
                
                # отключение кнопок
                self.m_window["-BUTTON_APPOINTMENTS_UPDATE-"].update(disabled=True)
                self.m_window["-BUTTON_APPOINTMENTS_DELETE-"].update(disabled=True)

            # если клик по ячейке
            else:
                # взятие данных из выделенной строки
                old_record = self.__data[self.__selected_cell[0]]

                # заполнение формы данными
                self.__set_record_form(old_record[1], old_record[3], old_record[4])

                # включение кнопок
                self.m_window["-BUTTON_APPOINTMENTS_UPDATE-"].update(disabled=False)
                self.m_window["-BUTTON_APPOINTMENTS_DELETE-"].update(disabled=False)

        # если клик по кнопке вставить
        elif event == "-BUTTON_APPOINTMENTS_INSERT-":
            # попытка взять данные с формы
            try:
                new_record = list(self.__get_record_form())

            except Exception as err:
                # обработка исключения
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                args = (None,)
                return (None, args)

            # замена name на id
            new_record[0] = int(self.__comboDoctorData.get_column("id", "name", new_record[0]))
            new_record[1] = int(self.__comboPatientData.get_column("id", "name", new_record[1]))

            # попытка отправить данные в бд
            try:
                db.appointment.insert(*new_record)

            except mysql.connector.IntegrityError as err:
                # обработка исключения
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                args = (None,)
                return (None, args)

            # взятие данных их бд
            self.__data = db.appointment.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)

        # если клик по кнопке обновить
        elif event == "-BUTTON_APPOINTMENTS_UPDATE-":
            if not self.__selected_cell:
                args = (None,)
                return (None, args)

            row, col = self.__selected_cell

            # берем данные выделенной строки
            old_record = self.__data[row]

            # на ее основе формируем данные для отправки
            new_record = list((old_record[0],) + self.__get_record_form())

            # замена name на id
            new_record[1] = int(self.__comboDoctorData.get_column("id", "name", new_record[1]))
            new_record[2] = int(self.__comboPatientData.get_column("id", "name", new_record[2]))

            # попытка отправить данные в бд
            try:
                db.appointment.update(*new_record)

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
            self.__data = db.appointment.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)

        # если клик по кнопке удалить
        elif event == "-BUTTON_APPOINTMENTS_DELETE-":
            if not self.__selected_cell:
                args = (None,)
                return (None, args)

            row, col = self.__selected_cell

            # берем данные выделенной строки
            old_record = self.__data[row]

            # попытка удалить данные из бд
            db.appointment.delete(old_record[0])
            
            # check results ???

            # удаление данных
            self.__data.remove(old_record)

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)

        args = (None,)
        return (None, args)
