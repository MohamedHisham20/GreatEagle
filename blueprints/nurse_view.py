from flask import request, jsonify, Blueprint
from flask_cors import CORS
from database import cursor

nurse_view = Blueprint("nurse_view", __name__, static_folder="static", template_folder="templates")
CORS(nurse_view, resources={
    r"/*": {"origins": "http://localhost:3000"}})  # Allow CORS for the login blueprint (Cross-Origin Resource Sharing

@nurse_view.route('/NurseProfile', methods=['POST'])
def nurse_profile():
    data = request.json
    print(data)
    NID = data.get('NID')

    # Initializing a dictionary to store the data
    nurse_data = {
        "patients": [],
        "medications": [],
        "doctors": []
    }

    # patients assigned to the nurse
    cursor.execute("""
        SELECT *
        FROM encounters 
        JOIN patients ON encounters.patientid = patients.nid
        WHERE encounters.dischargedatetime IS NULL 
        AND (encounters.morningnurseid = %s OR encounters.eveningnurseid = %s)
    """, (NID, NID))

    nurse_data["patients"] = cursor.fetchall()


    # medications assigned to the nurse's patients
    cursor.execute("""
        SELECT *
        FROM encounters 
        JOIN patients ON encounters.patientid = patients.nid
        JOIN medications ON medications.encounter = encounters.encounterid
        WHERE encounters.dischargedatetime IS NULL
        AND (encounters.morningnurseid = %s OR encounters.eveningnurseid = %s)
    """, (NID, NID))

    nurse_data["medications"] = cursor.fetchall()


    # displaying all the available doctors
    cursor.execute("""
        SELECT * FROM employee
        WHERE employee.dateleft IS NULL AND employee.role = 'Doctor' :: ROLE
    """)

    nurse_data["doctors"] = cursor.fetchall()

    return jsonify({"nurse_data": nurse_data})

