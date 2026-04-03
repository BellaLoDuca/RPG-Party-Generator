import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    missing_vars = []
    if not host:
        missing_vars.append("DB_HOST")
    if not user:
        missing_vars.append("DB_USER")
    if password is None:
        missing_vars.append("DB_PASSWORD")
    if not database:
        missing_vars.append("DB_NAME")

    if missing_vars:
        raise ValueError(
            "Missing database environment variables: "
            + ", ".join(missing_vars)
            + ". Check your .env file."
        )

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def fetch_races():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM races;")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def fetch_classes_for_role(role_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        c.class_id,
        c.class_type,
        c.strength,
        c.dexterity,
        c.constitution,
        c.intelligence,
        c.wisdom,
        c.charisma,
        r.role_name,
        cr.suitability_score
    FROM class_roles cr
    JOIN classes c ON cr.class_id = c.class_id
    JOIN roles r ON cr.role_id = r.role_id
    WHERE r.role_name = %s
    ORDER BY cr.suitability_score DESC;
    """

    cursor.execute(query, (role_name,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data