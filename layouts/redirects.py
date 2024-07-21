import PySimpleGUI as sg
import operator
import mysql

from datetime import datetime

from middleware.mysql import db

from .utils.combo_list_data import ComboListData

# ------ Redirects Layout ------
class RedirectsLayout:


    def __init__(self):
        # последняя выделенная ячейка таблицы
        self.__selected_cell = (0, 0)

        # номер столбца по которому сортируется таблица
        self.__order_by = 0

        # список отображающийся в графе пациент
        self.__comboPatientData = ComboListData()

        # список отображающийся в графе от врача
        self.__comboFromDoctorData = ComboListData()

        # список отображающийся в графе к врачу
        self.__comboToDoctorData = ComboListData()

        # список отображающийся в графе препарат
        self.__comboMedicationData = ComboListData()

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
        self.__data = db.redirect.select()

        patients = db.patient.select()

        doctors = db.doctor.select()

        medications = db.medication.select()

        if not patients:
            self.__comboPatientData.load_data({0 : "id", 1 : "name"}, [[-1, "NO PATIENTS"]])

        else:
            self.__comboPatientData.load_data({0 : "id", 1 : "name"}, patients)

        if not doctors:
            self.__comboFromDoctorData.load_data({0 : "id", 1 : "name"}, [[-1, "NO DOCTORS"]])
            self.__comboToDoctorData.load_data({0 : "id", 1 : "name"}, [[-1, "NO DOCTORS"]])

        else:
            self.__comboFromDoctorData.load_data({0 : "id", 1 : "name"}, doctors)
            self.__comboToDoctorData.load_data({0 : "id", 1 : "name"}, doctors)

        if not medications:
            self.__comboMedicationData.load_data({0 : "id", 1 : "title"}, [[-1, "NO MEDICATIONS"]])

        else:
            self.__comboMedicationData.load_data({0 : "id", 1 : "title"}, medications)

        # описание окна с таблицей карт
        redirects_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/Redirects",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_REDIRECTS_BACK-",
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
                    key="-INPUT_REDIRECTS_FIND_BY_NAME-",
                    enable_events=True,
                    expand_x=True
                )
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Id", "Patient", "From doctor", "Reason", "To doctor", "Date", "Diagnosis", "Prescribed medication"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=5,
                    key="-TABLE_REDIRECTS-",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True
                )
            ],
            [
                [
                    sg.Text(
                        text="Patient",
                        size=(7,)
                    ),
                    sg.Combo(
                        key="-COMBO_REDIRECTS_PATIENTS-",
                        values=self.__comboPatientData.get_combo_data(["name"]),
                        default_value=self.__comboPatientData.get_default_value(),
                        readonly=True,
                        expand_x=True
                    ),
                    sg.Button(
                        button_text="Find",
                        key="-BUTTON_REDIRECTS_PATIENT_PICKER-",
                        enable_events=True
                    )
                ],
                [
                    sg.Text(
                        text="From doctor",
                        size=(12,)
                    ),
                    sg.Combo(
                        key="-COMBO_REDIRECTS_FROM_DOCTOR-",
                        values=self.__comboFromDoctorData.get_combo_data(["name"]),
                        default_value=self.__comboFromDoctorData.get_default_value(),
                        readonly=True,
                        expand_x=True
                    ),
                    sg.Button(
                        button_text="Find",
                        key="-BUTTON_REDIRECTS_FROM_DOCTOR_PICKER-",
                        enable_events=True
                    )
                ],
                [
                    sg.Text(
                        text="Reason",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_REDIRECTS_REASON-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="To doctor",
                        size=(7,)
                    ),
                    sg.Combo(
                        key="-COMBO_REDIRECTS_TO_DOCTOR-",
                        values=self.__comboToDoctorData.get_combo_data(["name"]),
                        default_value=self.__comboToDoctorData.get_default_value(),
                        readonly=True,
                        expand_x=True
                    ),
                    sg.Button(
                        button_text="Find",
                        key="-BUTTON_REDIRECTS_TO_DOCTOR_PICKER-",
                        enable_events=True
                    )
                ],
                [
                    sg.Text(
                        text="Date",
                        size=(7,)
                    ),
                    sg.Input(
                        key="-INPUT_REDIRECTS_DATE-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Diagnosis",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_REDIRECTS_DIAGNOSIS-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Medication",
                        size=(10,)
                    ),
                    sg.Combo(
                        key="-COMBO_REDIRECTS_MEDICATION-",
                        values=self.__comboMedicationData.get_combo_data(["title"]),
                        default_value=self.__comboMedicationData.get_default_value(),
                        readonly=True,
                        expand_x=True
                    ),
                    sg.Button(
                        button_text="Find",
                        key="-BUTTON_REDIRECTS_MEDICATION_PICKER-",
                        enable_events=True
                    )
                ],
                [
                    sg.Button(
                        button_text="Insert",
                        key="-BUTTON_REDIRECTS_INSERT-",
                        enable_events=True
                    ),
                    sg.Button(
                        button_text="Update",
                        key="-BUTTON_REDIRECTS_UPDATE-",
                        enable_events=True,
                        disabled=True
                    ),
                    sg.Button(
                        button_text="Delete",
                        key="-BUTTON_REDIRECTS_DELETE-",
                        enable_events=True,
                        disabled=True
                    )
                ]
            ]
        ]

        # создание window
        self.m_window = sg.Window("Redirects", redirects_layout, resizable=True, finalize=True)

        if not patients:
            sg.popup_ok("Warning", "There is no any patients")
            self.m_window["-BUTTON_REDIRECTS_INSERT-"].update(disabled=True)

        if not doctors:
            sg.popup_ok("Warning", "There is no any doctors")
            self.m_window["-BUTTON_REDIRECTS_INSERT-"].update(disabled=True)

        if not medications:
            sg.popup_ok("Warning", "There is no any medications")
            self.m_window["-BUTTON_REDIRECTS_INSERT-"].update(disabled=True)

        return self.m_window




    # сбор данных с формы
    def __get_record_form(self) -> tuple:
        return (
            self.m_window["-COMBO_REDIRECTS_PATIENTS-"].get(),
            self.m_window["-COMBO_REDIRECTS_FROM_DOCTOR-"].get(),
            self.m_window["-INPUT_REDIRECTS_REASON-"].get(),
            self.m_window["-COMBO_REDIRECTS_TO_DOCTOR-"].get(),
            datetime.strptime(self.m_window["-INPUT_REDIRECTS_DATE-"].get(), "%Y.%m.%d %H:%M:%S"),
            self.m_window["-INPUT_REDIRECTS_DIAGNOSIS-"].get(),
            self.m_window["-COMBO_REDIRECTS_MEDICATION-"].get()
        )




    # запись данных в форму
    def __set_record_form(self, id_patients : int, id_from_doctor : int, reason : str, id_to_doctor : int, date : datetime, diagnosis : str, id_medication : int):
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.m_window["-COMBO_REDIRECTS_PATIENTS-"].update(value=id_patients)
        self.m_window["-COMBO_REDIRECTS_FROM_DOCTOR-"].update(value=id_from_doctor)
        self.m_window["-INPUT_REDIRECTS_REASON-"].update(value=reason)
        self.m_window["-COMBO_REDIRECTS_TO_DOCTOR-"].update(value=id_to_doctor)
        self.m_window["-INPUT_REDIRECTS_DATE-"].update(value=date.strftime("%Y.%m.%d %H:%M:%S"))
        self.m_window["-INPUT_REDIRECTS_DIAGNOSIS-"].update(value=diagnosis)
        self.m_window["-COMBO_REDIRECTS_MEDICATION-"].update(value=id_medication)




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




    def set_patient_name(self, name : str):
        if not name:
            name = self.__comboPatientData.get_default_value()

        self.m_window["-COMBO_REDIRECTS_PATIENTS-"].update(value=name)

    def set_from_doctor_name(self, name : str):
        if not name:
            name = self.__comboFromDoctorData.get_default_value()

        self.m_window["-COMBO_REDIRECTS_FROM_DOCTOR-"].update(value=name)

    def set_to_doctor_name(self, name : str):
        if not name:
            name = self.__comboToDoctorData.get_default_value()

        self.m_window["-COMBO_REDIRECTS_TO_DOCTOR-"].update(value=name)

    def set_medication_name(self, name : str):
        if not name:
            name = self.__comboMedicationData.get_default_value()

        self.m_window["-COMBO_REDIRECTS_MEDICATION-"].update(value=name)

    # обработчик событий приложения
    def events_handler(self, event, values):
        # если клик по кнопке назад или закрытие окна
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_REDIRECTS_BACK-":
            self.m_window.close()
            # отправляем команду
            args = (None,)
            return ("menu", args)

        elif event == "-BUTTON_REDIRECTS_PATIENT_PICKER-":
            args = (None,)

            # открытие окна просмотрщика пациентов
            return ("patient_picker", args)

        elif event == "-BUTTON_REDIRECTS_FROM_DOCTOR_PICKER-":
            args = ("from_doctor_picker",)

            # открытие окна просмотрщика врача
            return ("doctor_picker", args)

        elif event == "-BUTTON_REDIRECTS_TO_DOCTOR_PICKER-":
            args = ("to_doctor_picker",)

            # открытие окна просмотрщика врача
            return ("doctor_picker", args)

        elif event == "-BUTTON_REDIRECTS_MEDICATION_PICKER-":
            args = (None,)

            # открытие окна просмотрщика препаратов
            return ("medication_picker", args)

        # вводим поиск
        elif event == "-INPUT_REDIRECTS_FIND_BY_NAME-":
            name = self.m_window["-INPUT_REDIRECTS_FIND_BY_NAME-"].get()

            length = len(name)

            # поиск по первой букве
            if length == 1:
                # взятие данных из бд
                self.__data = db.redirect.find_by_name_with_names("{}%".format(name))

            # поиск по всему полю
            elif length > 1:
                # взятие данных из бд
                self.__data = db.redirect.find_by_name_with_names("%{}%".format(name))

            # ничего не ищем
            else:
                # взятие данных из бд
                self.__data = db.redirect.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_REDIRECTS-"].update(self.__data)

        # если клик по таблице
        elif event[0] == "-TABLE_REDIRECTS-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # если клик по заголовку таблицы
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_REDIRECTS-"].update(self.__data)

            # если клик не по ячейке или заголовку таблицы
            elif row is None or col is None:
                self.__selected_cell = None

                # сброс данных в форме
                self.__set_record_form(*(self.__comboPatientData.get_default_value(), self.__comboFromDoctorData.get_default_value(), "", self.__comboToDoctorData.get_default_value(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "", self.__comboMedicationData.get_default_value()))

                # снятие выделения
                self.m_window["-TABLE_REDIRECTS-"].update(select_rows=[])
                
                # отключение кнопок
                self.m_window["-BUTTON_REDIRECTS_UPDATE-"].update(disabled=True)
                self.m_window["-BUTTON_REDIRECTS_DELETE-"].update(disabled=True)

            ## если клик по ячейке с пациентом
            #elif col == 1:
            #    # получаем данные о пациенте
            #    line = db.patient.find_by_name(self.__data[row][col])[0]

            #    # получаем id
            #    id = line[0]
                
            #    # формируем параметры инициализации окна
            #    args = (id,)

            #    # открытие дополнительного окна с информацией
            #    return ("patient_info", args)

            # если клик по ячейке с препаратом
            elif col == 7:
                # получаем данные о препарате
                line = db.medication.find_by_name(self.__data[row][col])[0]

                # получаем id
                id = line[0]
                
                # формируем параметры инициализации окна
                args = (id,)

                # открытие дополнительного окна с информацией
                return ("medication_info", args)

            # если клик по ячейке
            else:
                # взятие данных из выделенной строки
                old_record = self.__data[self.__selected_cell[0]]

                # заполнение формы данными
                self.__set_record_form(*old_record[1:])

                # включение кнопок
                self.m_window["-BUTTON_REDIRECTS_UPDATE-"].update(disabled=False)
                self.m_window["-BUTTON_REDIRECTS_DELETE-"].update(disabled=False)

        # если клик по кнопке вставить
        elif event == "-BUTTON_REDIRECTS_INSERT-":
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

            # замена name пациента на id
            new_record[0] = int(self.__comboPatientData.get_column("id", "name", new_record[0]))

            # замена name от врача на id
            new_record[1] = int(self.__comboFromDoctorData.get_column("id", "name", new_record[1]))

            # замена name к врачу на id
            new_record[3] = int(self.__comboToDoctorData.get_column("id", "name", new_record[3]))

            # замена title на id
            new_record[6] = int(self.__comboMedicationData.get_column("id", "title", new_record[6]))

            # попытка отправить данные в бд
            try:
                db.redirect.insert(*new_record)

            except mysql.connector.IntegrityError as err:
                # обработка исключения
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                args = (None,)
                return (None, args)

            # взятие данных их бд
            self.__data = db.redirect.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_REDIRECTS-"].update(self.__data)

        # если клик по кнопке обновить
        elif event == "-BUTTON_REDIRECTS_UPDATE-":
            if not self.__selected_cell:
                args = (None,)
                return (None, args)

            row, col = self.__selected_cell

            # берем данные выделенной строки
            old_record = self.__data[row]

            # на ее основе формируем данные для отправки
            new_record = list((old_record[0],) + self.__get_record_form())

            # замена name пациента на id
            new_record[1] = int(self.__comboPatientData.get_column("id", "name", new_record[1]))

            # замена name от врача на id
            new_record[2] = int(self.__comboFromDoctorData.get_column("id", "name", new_record[2]))

            # замена name к врачу на id
            new_record[4] = int(self.__comboToDoctorData.get_column("id", "name", new_record[4]))

            # замена title на id
            new_record[7] = int(self.__comboMedicationData.get_column("id", "title", new_record[7]))

            # попытка отправить данные в бд
            try:
                db.redirect.update(*new_record)

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
            self.__data = db.redirect.select()

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_REDIRECTS-"].update(self.__data)

        # если клик по кнопке удалить
        elif event == "-BUTTON_REDIRECTS_DELETE-":
            if not self.__selected_cell:
                args = (None,)
                return (None, args)

            row, col = self.__selected_cell

            # берем данные выделенной строки
            old_record = self.__data[row]

            # попытка удалить данные из бд
            db.redirect.delete(old_record[0])
            
            # check results ???

            # удаление данных
            self.__data.remove(old_record)

            # сортировка таблицы
            self.__sort_table((self.__order_by, 0))

            # обновление данных в таблице
            self.m_window["-TABLE_REDIRECTS-"].update(self.__data)

        args = (None,)
        return (None, args)
