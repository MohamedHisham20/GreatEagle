import psycopg2.extras
from flask import jsonify

# Database connection
database_session = psycopg2.connect(
    database="IseeUDB",
    user="IseeUDB_owner",
    password="o70CUtSaXsJK",
    host="ep-still-truth-a21z0m3n.eu-central-1.aws.neon.tech",
    port="5432"
)
cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)


def execute_query(query, params):
    try:
        cursor.execute(query, params)
        database_session.commit()
        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        database_session.rollback()
        print(f"Error during registration: {e}")  # Log the error to the console for debugging
        return jsonify({"error": str(e)}), 500
