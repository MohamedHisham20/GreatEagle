from flask import request, jsonify, Blueprint
from flask_cors import CORS
from database import cursor, database_session

doctor_view = Blueprint("doctor_view", __name__, static_folder="static", template_folder="templates")
CORS(doctor_view, resources={
    r"/*": {"origins": "http://localhost:3000"}})  # Allow CORS for the login blueprint (Cross-Origin Resource Sharing


@doctor_view.route('/doctor/report', methods=['POST'])
def doc_report():
    # add report for the patient from the doctor (after the doctor click on the submit button in add report page)
    data = request.json
    print(data)
    bed_id = data.get('bed_id')
    report = data.get('report')
    reporter_doc = report.get('reportdoc')
    notes = report.get('notes')
    curr_time = data.get('currentTime')
    medication = data.get('medications')
    investigation = data.get('investigations')

    #############        check      #################
    # get the encounter id from the bed id
    cursor.execute("SELECT encounterid FROM encounters WHERE bedid = %s AND dischargedatetime IS NULL", (bed_id,))
    encounter_id = cursor.fetchone()

    # create the initial report to get the report_id
    initial_report_query = """INSERT INTO reports (notes, reportdoctorid, encounter) 
                            VALUES (%s, %s, %s) RETURNING reportid"""
    initial_report_params = (notes, reporter_doc, encounter_id)
    cursor.execute(initial_report_query, initial_report_params)
    report_id = cursor.fetchone()[0]

    medication_flag = doc_medications(report_id, encounter_id, medication)
    investigation_flag = doc_investigation(report_id, encounter_id, investigation)

    # update the report with the flags of it
    update_report_query = "UPDATE reports SET medicationflag = %s, scansflag = %s WHERE reportid = %s"
    update_report_params = (medication_flag, investigation_flag, report_id)
    cursor.execute(update_report_query, update_report_params)

    # update lastcheckup time with currentTime
    update_encounter_query = "UPDATE encounters SET lastcheckup = %s WHERE encounterid = %s"
    update_encounter_params = (curr_time, encounter_id)
    cursor.execute(update_encounter_query, update_encounter_params)

    database_session.commit()
    return jsonify({"message": "Report added successfully"}), 200


def doc_investigation(report_id, encounter_id, investigation):
    """

        :param investigation:
        :param encounter_id:
        :param report_id: the report to be put in the investigation        :param investigation:  string
        :return: true or false if there's an investigation
    """
    if investigation:
        # add the investigation to the patient and return true
        # get the investigation data
        invname = investigation.get('invname')
        invdatetime = investigation.get('invdatetime')
        orderedby = investigation.get('orderedby')

        # add the investigation to the database
        investigation_query = """INSERT INTO investigations (invname, invdatetime, orderedby, encounter, report) 
                                VALUES (%s, %s, %s, %s, %s)"""
        investigation_params = (invname, invdatetime, orderedby, encounter_id, report_id)
        cursor.execute(investigation_query, investigation_params)
        database_session.commit()
        jsonify({"message": "Investigation added successfully"}), 200
        return True
    return False


def doc_medications(report_id, encounter_id, medication):
    if medication:
        # get the medication data
        name = medication.get('name')
        dosage = medication.get('dosage')
        dosecount = medication.get('dosecount')
        assigndatetime = medication.get('assigndatetime')
        frequencyperday = medication.get('frequencyperday')

        # add the medication to the database
        medication_query = """INSERT INTO medications 
                            (name, dosage, dosecount, assigndatetime, frequencyperday, encounter, report)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        medication_params = (name, dosage, dosecount, assigndatetime, frequencyperday, encounter_id, report_id)
        cursor.execute(medication_query, medication_params)
        database_session.commit()
        jsonify({"message": "Medication added successfully"}), 200
        return True
    return False


@doctor_view.route('/doctor/current_encounters', methods=['GET'])
def current_encounters():  # view all active patients ( dischargedatetime in encounters is NULL)
    cursor.execute("""
        SELECT *
        FROM encounters JOIN patients ON encounters.patientid = patients.nid
        WHERE encounters.dischargedatetime IS NULL
    """)
    active_encounters = cursor.fetchall()
    return jsonify({"active_encounters": active_encounters})


@doctor_view.route('/doctor/current_employees', methods=['GET'])
def current_employees():  # View all active employees (role should be either doctor or nurse)
    cursor.execute("""
        SELECT * FROM employee
        WHERE employee.dateleft IS NULL AND (employee.role = 'Doctor' :: ROLE OR employee.role = 'Nurse' :: ROLE)
    """)
    active_employees = cursor.fetchall()
    return jsonify({"active_employees": active_employees})

@doctor_view.route('/doctor/doctor_investigations', methods=['POST'])
def doctor_investigations():
    data = request.json
    print(data)
    DID = data.get('DID')
    cursor.execute("""
        SELECT * 
        FROM investigations
        WHERE orderedby = %s
    """, (DID,))
    investigations = cursor.fetchall()
    return jsonify({"doctor_investigations": investigations})

@doctor_view.route('/doctor/doctor_reports', methods=['POST'])
def doctor_reports():
    data = request.json
    print(data)
    DID = data.get('DID')
    cursor.execute("""
        SELECT p.ppic,p.fname, p.lname, e.bedid, r.*
        FROM reports r JOIN encounters e on e.encounterid = r.encounter
        JOIN patients p ON p.nid = e.patientid
        WHERE r.reportdoctorid = %s
    """, (DID,))
    reports = cursor.fetchall()
    return jsonify({"doctor_reports": reports})

#discharge patient
@doctor_view.route('/doctor/discharge', methods=['POST'])
def discharge():
    data = request.json
    print(data)
    bed_id = data.get('BID')
    curr_time = data.get('currentTime')
    discharge_doc_id = data.get('doctor_id')
    print(discharge_doc_id)
    cursor.execute("""
        UPDATE encounters
        SET dischargedatetime = %s, dischargedoctorid = %s
        WHERE bedid = %s AND dischargedatetime IS NULL
    """, (curr_time, discharge_doc_id, bed_id))
    database_session.commit()
    return jsonify({"message": "discharged successfully"}), 200
