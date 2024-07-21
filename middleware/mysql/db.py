import mysql.connector
import sqlite3

from .doctors import Doctors
from .patients import Patients
from .appointments import Appointments
from .medical_records import MedicalRecords
from .redirects import Redirects
from .diagnosis_history import DiagnosisHistory
from .complaints_history import ComplaintsHistory
from .gender_type import GenderType
from .disability_types import DisabilityType
from .medications import Medications
from .general_info import GeneralInfo

from .db_placeholder import DbPlaceholder

# устанавливаем соединение с бд
# mydb = mysql.connector.connect(
#   host="192.168.0.108",
#   user="ismi",
#   password="ismi",
#   database='ismi'
# )
mydb = sqlite3.connect('ismi.db')

# берем курсор
cursor = mydb.cursor()

# создаем объекты и передаем в них данные о соединении бд
gender_type = GenderType(mydb, cursor)
# создаем таблицы
gender_type.create()
# добавляем полы
gender_type.insert("Female")
gender_type.insert("Male")

disability_type = DisabilityType(mydb, cursor)
# создаем таблицы
disability_type.create()
# добавляем полы
disability_type.insert("None")
disability_type.insert("I")
disability_type.insert("II")
disability_type.insert("III")
disability_type.insert("IV")

doctor = Doctors(mydb, cursor)
# создаем таблицы
doctor.create()

patient = Patients(mydb, cursor)
# создаем таблицы
patient.create()

appointment = Appointments(mydb, cursor)
# создаем таблицы
appointment.create()

medical_record = MedicalRecords(mydb, cursor)
# создаем таблицы
medical_record.create()

medication = Medications(mydb, cursor)
# создаем таблицы
medication.create()

redirect = Redirects(mydb, cursor)
# создаем таблицы
redirect.create()

diagnosis_history = DiagnosisHistory(mydb, cursor)

complaints_history = ComplaintsHistory(mydb, cursor)

general_info = GeneralInfo(mydb, cursor)
