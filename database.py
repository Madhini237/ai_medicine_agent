import sqlite3

DB_NAME = "patients.db"

def create_tables():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        chat_id TEXT UNIQUE,
        disease TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        medicine_name TEXT,
        reminder_time TEXT,
        confirmed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_patient(name, chat_id, disease):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO patients(name,chat_id,disease) VALUES(?,?,?)",
        (name, chat_id, disease)
    )

    conn.commit()
    conn.close()


def get_patient(chat_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE chat_id=?", (chat_id,))
    patient = cursor.fetchone()

    conn.close()
    return patient


def add_medicine(patient_id, medicine_name, time):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO medicines(patient_id,medicine_name,reminder_time) VALUES(?,?,?)",
        (patient_id, medicine_name, time)
    )

    conn.commit()
    conn.close()


def get_all_medicines():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT patients.chat_id, patients.name,
           medicines.medicine_name, medicines.reminder_time
    FROM medicines
    JOIN patients ON medicines.patient_id = patients.id
    """)

    data = cursor.fetchall()

    conn.close()
    return data