import PySimpleGUI as sg

# ------ Menu Layout ------
class MenuLayout:
    def __init__(self):
        self.m_window = None

        self.window()

    # создаем window и храним его в self.m_window
    def window(self):
        if self.m_window:
            return self.m_window

        # описание меню window
        menu_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Doctors",
                    auto_size_button=True,
                    key='-BUTTON_DOCTORS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                ),
                sg.Button(
                    button_text="Patients",
                    auto_size_button=True,
                    key='-BUTTON_PATIENTS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                ),
                sg.Button(
                    button_text="Medications",
                    auto_size_button=True,
                    key='-BUTTON_MEDICATIONS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                )
            ],
            [
                sg.Button(
                    button_text="Appointments",
                    auto_size_button=True,
                    key='-BUTTON_APPOINTMENTS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                ),
                sg.Button(
                    button_text="Medical records",
                    auto_size_button=True,
                    key='-BUTTON_MEDICAL_RECORDS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                ),
                sg.Button(
                    button_text="Redirects",
                    auto_size_button=True,
                    key='-BUTTON_REDIRECTS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                ),
            ],
            [
                sg.Button(
                    button_text="Diagnosis history",
                    auto_size_button=True,
                    key='-BUTTON_DIAGNOSIS_HISTORY-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                ),
                sg.Button(
                    button_text="Complaints history",
                    auto_size_button=True,
                    key='-BUTTON_COMPLAINTS_HISTORY-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                )
            ],
            [
                sg.Button(
                    button_text="General information",
                    auto_size_button=True,
                    key='-BUTTON_GENERAL_INFO-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                )
            ]
        ]

        # создание window
        self.m_window = sg.Window("Menu", menu_layout, resizable=True, finalize=True)

        return self.m_window


    # обработчик событий приложения
    def events_handler(self, event, values):
        # если событие закрытия
        if (event == sg.WIN_CLOSED or event == "Cancel"):
            args = (None,)
            return ("exit", args)

        # если хотим зайти в таблицу с докторами
        elif event == "-BUTTON_DOCTORS-":
            self.m_window.hide()
            args = (None,)
            return ("doctors", args)

        # если хотим зайти в таблицу с пациентами
        elif event == "-BUTTON_PATIENTS-":
            self.m_window.hide()
            args = (None,)
            return ("patients", args)

        # если хотим зайти в таблицу с медикаментами
        elif event == "-BUTTON_MEDICATIONS-":
            self.m_window.hide()
            args = (None,)
            return ("medications", args)

        # если хотим зайти в таблицу с записями
        elif event == "-BUTTON_APPOINTMENTS-":
            self.m_window.hide()
            args = (None,)
            return ("appointments", args)

        # если хотим зайти в таблицу с картами
        elif event == "-BUTTON_MEDICAL_RECORDS-":
            self.m_window.hide()
            args = (None,)
            return ("medical_records", args)

        # если хотим зайти в таблицу с направлениями
        elif event == "-BUTTON_REDIRECTS-":
            self.m_window.hide()
            args = (None,)
            return ("redirects", args)

        # если хотим посмотреть истории диагнозов
        elif event == "-BUTTON_DIAGNOSIS_HISTORY-":
            self.m_window.hide()
            args = (None,)
            return ("diagnosis_history", args)

        # если хотим посмотреть истории жалоб
        elif event == "-BUTTON_COMPLAINTS_HISTORY-":
            self.m_window.hide()
            args = (None,)
            return ("complaints_history", args)

        # если хотим посмотреть общую информацию
        elif event == "-BUTTON_GENERAL_INFO-":
            self.m_window.hide()
            args = (None,)
            return ("general_info", args)
