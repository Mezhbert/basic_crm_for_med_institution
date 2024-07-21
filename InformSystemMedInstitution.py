from colorsys import rgb_to_hls
import PySimpleGUI as sg

# import layouts classes
from layouts.menu import MenuLayout
from layouts.doctors import DoctorsLayout
from layouts.patients import PatientsLayout
from layouts.medications import MedicationsLayout
from layouts.appointments import AppointmentsLayout
from layouts.medical_records import MedicalRecordsLayout
from layouts.redirects import RedirectsLayout
from layouts.diagnosis_history import DiagnosisHistoryLayout
from layouts.complaints_history import ComplaintsHistoryLayout

from layouts.patient_info import PatientInfoLayout
from layouts.medication_info import MedicationInfoLayout

from layouts.doctor_picker import DoctorPickerLayout
from layouts.patient_picker import PatientPickerLayout
from layouts.medication_picker import MedicationPickerLayout
from layouts.general_info import GeneralInfoLayout


# add a touch of color
sg.theme("DarkTeal7")

sg.set_options(font=('Arial Bold', 16))

# точка входа в программу
def main():
    # создание меню layout
    menu_layout = MenuLayout()

    # объявляем переменные для хранения остальных layout
    doctors_layout = None
    patients_layout = None
    medications_layout = None
    appointments_layout = None
    medical_records_layout = None
    redirects_layout = None
    diagnosis_history_layout = None
    complaints_history_layout = None

    general_info_layout = None

    patient_info_layout = None
    medication_info_layout = None

    doctor_picker_layout = None
    patient_picker_layout = None
    medication_picker_layout = None

    # геттер упрощающий получить layout который привязан к window
    def get_layout(window : sg.Window):
        layouts = [menu_layout, doctors_layout, patients_layout, medications_layout, appointments_layout, medical_records_layout, redirects_layout, diagnosis_history_layout, complaints_history_layout, patient_info_layout, medication_info_layout, doctor_picker_layout, patient_picker_layout, medication_picker_layout, general_info_layout]

        for layout in layouts:
            if not layout:
                continue

            if layout.window() == window:
                return layout

        return None

    def get_name(window : sg.Window):
        names = { menu_layout : "menu", doctors_layout : "doctors", patients_layout : "patients", medications_layout : "medications", appointments_layout : "appointments", medical_records_layout : "medical_records", redirects_layout : "redirects", diagnosis_history_layout : "diagnosis_history", complaints_history_layout : "", patient_info_layout : "patient_info", medication_info_layout : "medication_info", doctor_picker_layout : "doctor_picker", patient_picker_layout : "patient_picker", medication_picker_layout : "medication_picker", general_info_layout : "general_info" }

        return names[window]

    # цикл событий для обработки событий и получения пользовательского ввода
    while True:
        # чтение окон, событий, значений
        window, event, values = sg.read_all_windows()
    
        layout = get_layout(window)

        if not layout:
            print("layout not found")
            break

        # получение команды перехода или закрытия от текущего layout
        cmd, args = layout.events_handler(event, values)

        # если команда пришла от окна меню
        if layout == menu_layout:
            if cmd == "exit":
                break

            # если команда doctors
            elif cmd == "doctors":
                doctors_layout = DoctorsLayout()

            # если команда patients
            elif cmd == "patients":
                patients_layout = PatientsLayout()
                pass

            # если команда medications
            elif cmd == "medications":
                medications_layout = MedicationsLayout()
                pass

            # если команда appointments
            elif cmd == "appointments":
                appointments_layout = AppointmentsLayout()
                pass

            # если команда medical_records
            elif cmd == "medical_records":
                medical_records_layout = MedicalRecordsLayout()
                pass

            # если команда redirects
            elif cmd == "redirects":
                redirects_layout = RedirectsLayout()
                pass

            # если команда diagnosis_history
            elif cmd == "diagnosis_history":
                diagnosis_history_layout = DiagnosisHistoryLayout()
                pass

            # если команда complaints_history
            elif cmd == "complaints_history":
                complaints_history_layout = ComplaintsHistoryLayout()
                pass

            # если команда general_info
            elif cmd == "general_info":
                general_info_layout = GeneralInfoLayout()
                pass

        # иначе, если команда пришла от окон привязанных к одному из нижних layout
        elif layout in [doctors_layout, patients_layout, appointments_layout, medical_records_layout, medications_layout, redirects_layout, diagnosis_history_layout, complaints_history_layout, general_info_layout]:
            # если команда exit/menu
            if cmd in ["exit", "menu"]:
                # скрываем окно
                menu_layout.window().un_hide()

            elif cmd == "patient_info":
                patient_info_layout = PatientInfoLayout(*args)

            elif cmd == "medication_info":
                medication_info_layout = MedicationInfoLayout(*args)

            elif cmd == "doctor_picker":
                doctor_picker_layout = DoctorPickerLayout(get_name(layout), args[0])

            elif cmd == "patient_picker":
                patient_picker_layout = PatientPickerLayout(get_name(layout))

            elif cmd == "medication_picker":
                medication_picker_layout = MedicationPickerLayout(get_name(layout))

        # иначе, если команда пришла от информационных окон
        elif layout in [patient_info_layout, medication_info_layout]:
            pass

        elif layout == doctor_picker_layout:
            if cmd == "picked_doctor":
                if args[1] == "appointments":
                    appointments_layout.set_doctor_name(args[0])

                elif args[1] == "redirects":

                    # checking for which column
                    if args[2] == "from_doctor_picker":
                        redirects_layout.set_from_doctor_name(args[0])

                    elif args[2] == "to_doctor_picker":
                        redirects_layout.set_to_doctor_name(args[0])

        elif layout == patient_picker_layout:
            if cmd == "picked_patient":
                if args[1] == "appointments":
                    appointments_layout.set_patient_name(args[0])

                elif args[1] == "medical_records":
                    medical_records_layout.set_patient_name(args[0])

                elif args[1] == "redirects":
                    redirects_layout.set_patient_name(args[0])

        elif layout == medication_picker_layout:
            if cmd == "picked_medication":
                if args[1] == "medical_records":
                    medical_records_layout.set_medication_name(args[0])

                elif args[1] == "redirects":
                    redirects_layout.set_medication_name(args[0])

    # закрытие окна меню если получили команду exit от меню layout
    menu_layout.window().close()

if __name__ == '__main__':
    main()
