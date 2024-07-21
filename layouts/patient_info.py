import PySimpleGUI as sg
import operator
import mysql

from middleware.mysql import db

# ------ Patient_info Layout ------
class PatientInfoLayout:


    def __init__(self, id : int):
        # id пациента
        self.__id = id

        self.m_window = None

        # создаем window и храним его в self.m_window
        self.window()




    # создаем window и храним его в self.m_window
    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        # получение всех данных из бд
        patient_info = db.patient.find_by_id(self.__id)[0]
        medical_records = db.medical_record.find_by_patient_id(self.__id)

        # описание окна с информацией о пациенте
        patient_info_layout = [
            [
                [
                    sg.Text(
                        text="Id",
                        size=(5,)
                    ),
                    sg.Input(
                        default_text=patient_info[0],
                        key="-INPUT_PATIENT_INFO_ID-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Name",
                        size=(5,)
                    ),
                    sg.Input(
                        default_text=patient_info[1],
                        key="-INPUT_PATIENT_INFO_NAME-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Birthdate",
                        size=(5,)
                    ),
                    sg.Input(
                        default_text=patient_info[2],
                        key="-INPUT_PATIENT_INFO_BIRTHDATE-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Phone",
                        size=(5,)
                    ),
                    sg.Input(
                        default_text=patient_info[3],
                        key="-INPUT_PATIENT_INFO_PHONE-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Gender",
                        size=(5,)
                    ),
                    sg.Input(
                        default_text=patient_info[4],
                        key="-INPUT_PATIENT_INFO_GENDER-",
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
                        default_text=patient_info[5],
                        key="-INPUT_PATIENT_INFO_WEIGHT-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Height",
                        size=(5,)
                    ),
                    sg.Input(
                        default_text=patient_info[6],
                        key="-INPUT_PATIENT_INFO_HEIGHT-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Disability",
                        size=(7,)
                    ),
                    sg.Input(
                        default_text=patient_info[7],
                        key="-INPUT_PATIENT_INFO_DISABILITY-",
                        readonly=True,
                        expand_x=True
                    )
                ]
            ],
            [
                sg.Table(
                    values=medical_records,
                    headings=["Id", "Date", "Complaints", "Diagnosis", "Allergy", "Treatment", "Prescribed medication"],
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
            ]
        ]

        # создание window
        self.m_window = sg.Window("Patient info", patient_info_layout, resizable=True, finalize=True)

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

        args = (None,)
        return (None, args)
