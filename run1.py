from flask import Flask
from sqlalchemy import URL, create_engine

app = Flask(__name__)

connection_string = URL.create(
  'postgresql',
  username='neondb_owner',
  password='nafA0yCgl2jH',
  host='ep-bitter-surf-a2u091xk.eu-central-1.aws.neon.tech',
  database='neondb'
)
engine = create_engine(connection_string)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)


# def insert_rowss():
#     for i in range(15):
#         # Dummy data for the insert statement
#         invname = f"Test Investigation {i}"
#         invdatetime = "2022-01-01 00:00:00"  # Use a proper datetime string here
#         orderedby = "Test Doctor"
#         encounter_id = 1  # Use a valid encounter_id here
#         report_id = 1  # Use a valid report_id here
#
#         # Insert statement
#         investigation_query = """
#             INSERT INTO investigations (invname, invdatetime, orderedby, encounter, report)
#             VALUES (%s, %s, %s, %s, %s)
#         """
#         investigation_params = (invname, invdatetime, orderedby, encounter_id, report_id)
#         cursor.execute(investigation_query, investigation_params)
#
#     # Commit the transaction
#     database_session.commit()
#
# def insert_rows():
#     for i in range(15):
#         # Dummy data for the insert statement
#         encounter_id = str(i + 31)  # Use a valid encounter_id here
#         notes = f"Test Notes {i}"
#         scans_flag = False
#         medication_flag = False
#         report_doctor_id = 'D001'  # Use a valid doctor_id here
#
#         # Insert statement for Reports
#         report_query = """
#             INSERT INTO Reports (encounter, Notes, ScansFlag, MedicationFlag, ReportDoctorID)
#             VALUES (%s, %s, %s, %s, %s)
#         """
#         report_params = (encounter_id, notes, scans_flag, medication_flag, report_doctor_id)
#         # cursor.execute(report_query, report_params)
#
#         # Dummy data for Investigations
#         inv_type = "Lab"  # Use a valid investigation type here
#         inv_name = f"Test Investigation {i}"
#         result = "Positive"
#         inv_datetime = "2022-01-01 00:00:00"  # Use a proper datetime string here
#         ordered_by = 'D002'  # Use a valid doctor_id here
#         # reviewed_by = 1  # Use a valid doctor_id here
#         notes = f"Test Notes {i}"
#
#         # Insert statement for Investigations
#         investigation_query = """
#             INSERT INTO Investigations (encounter, InvName, Result, InvDateTime, OrderedBy, Notes)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         investigation_params = (encounter_id, inv_name, result, inv_datetime, ordered_by, notes)
#         # cursor.execute(investigation_query, investigation_params)
#
#         # Dummy data for Medications
#         name = f"Test Medication {i}"
#         dosage = "1 tablet"
#         dose_count = random.random() * 10
#         # last_dose_time = "2022-01-01 00:00:00"  # Use a proper datetime string here
#         assign_date_time = "2022-01-01 00:00:00"  # Use a proper datetime string here
#         frequency_per_day = random.randint(1, 4)
#
#         # Insert statement for Medications
#         medication_query = """
#             INSERT INTO Medications (Encounter, Name, Dosage, DoseCount, AssignDateTime, FrequencyPerDay)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         medication_params = (encounter_id, name, dosage, dose_count, assign_date_time, frequency_per_day)
#         cursor.execute(medication_query, medication_params)
#
#     # Commit the transaction
#     database_session.commit()
#     return "Data inserted successfully"
# insert_rows()
