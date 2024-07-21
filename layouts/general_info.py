import PySimpleGUI as sg
import operator
import mysql

from middleware.mysql import db

# ------ General info Layout ------
class GeneralInfoLayout:


    def __init__(self):
        self.m_window = None

        # создаем window и храним его в self.m_window
        self.window()




    # создаем window и храним его в self.m_window
    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        # получение всех данных из бд
        number_of_doctors = db.general_info.count_doctors()
        number_of_patients = db.general_info.count_patients()
        number_of_patients_without_disability = db.general_info.count_patients_without_disablity()
        number_of_patients_with_1_disability = db.general_info.count_patients_with_1_disablity()
        number_of_patients_with_2_disability = db.general_info.count_patients_with_2_disablity()
        number_of_patients_with_3_disability = db.general_info.count_patients_with_3_disablity()
        number_of_patients_with_4_disability = db.general_info.count_patients_with_4_disablity()
        number_of_medications = db.general_info.count_medications()

        # описание окна с общей информацией
        general_info_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/General info",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_GENERAL_INFO_BACK-",
                    expand_x=True,
                    expand_y=False,
                    enable_events=True
                )
            ],
            [
                [
                    sg.Text(
                        text="Number of doctors",
                        size=(40,)
                    ),
                    sg.Input(
                        default_text=number_of_doctors,
                        key="-INPUT_NUMBER_OF_DOCTORS-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Number of patients",
                        size=(40,)
                    ),
                    sg.Input(
                        default_text=number_of_patients,
                        key="-INPUT_NUMBER_OF_PATIENTS-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Number of patients without a disability category",
                        size=(40,)
                    ),
                    sg.Input(
                        default_text=number_of_patients_without_disability,
                        key="-INPUT_NUMBER_OF_PATIENTS_WITHOUT_DISABILITY-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Number of patients with 1 disability category",
                        size=(40,)
                    ),
                    sg.Input(
                        default_text=number_of_patients_with_1_disability,
                        key="-INPUT_NUMBER_OF_PATIENTS_WITH_1_DISABILITY-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Number of patients with 2 disability category",
                        size=(40,)
                    ),
                    sg.Input(
                        default_text=number_of_patients_with_2_disability,
                        key="-INPUT_NUMBER_OF_PATIENTS_WITH_2_DISABILITY-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Number of patients with 3 disability category",
                        size=(40,)
                    ),
                    sg.Input(
                        default_text=number_of_patients_with_3_disability,
                        key="-INPUT_NUMBER_OF_PATIENTS_WITH_3_DISABILITY-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Number of patients with 4 disability category",
                        size=(40,)
                    ),
                    sg.Input(
                        default_text=number_of_patients_with_4_disability,
                        key="-INPUT_NUMBER_OF_PATIENTS_WITH_4_DISABILITY-",
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Number of medications",
                        size=(40,)
                    ),
                    sg.Input(
                        default_text=number_of_medications,
                        key="-INPUT_NUMBER_OF_MEDICATIONS-",
                        readonly=True,
                        expand_x=True
                    )
                ]
            ]
        ]

        # создание window
        self.m_window = sg.Window("General info", general_info_layout, resizable=True, finalize=True)

        return self.m_window





    # обработчик событий приложения
    def events_handler(self, event, values):
        # если клик по кнопке назад или закрытие окна
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_GENERAL_INFO_BACK-":
            self.m_window.close()
            # отправляем команду
            args = (None,)
            return ("menu", args)

        args = (None,)
        return (None, args)
