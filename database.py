"""
database.py — SQLite database initialization and helper functions
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "health.db")


def get_db():
    """Return a new database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # Rows accessible by column name
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables and seed sample doctors if not present."""
    conn = get_db()
    c = conn.cursor()

    # ── Users ──────────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name     TEXT    NOT NULL,
            age           INTEGER,
            gender        TEXT,
            email         TEXT    UNIQUE NOT NULL,
            phone         TEXT,
            password_hash TEXT    NOT NULL,
            created_at    DATETIME DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Health Profiles ────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS health_profiles (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id             INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
            height              REAL,
            weight              REAL,
            bmi                 REAL,
            blood_group         TEXT,
            blood_pressure      TEXT,
            blood_sugar         REAL,
            heart_rate          INTEGER,
            body_temperature    REAL,
            existing_diseases   TEXT,
            allergies           TEXT,
            current_medications TEXT,
            smoking_habit       TEXT,
            alcohol_consumption TEXT,
            exercise_frequency  TEXT,
            sleeping_hours      REAL,
            updated_at          DATETIME DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Doctors ────────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT    NOT NULL,
            specialization TEXT,
            qualification  TEXT,
            experience     INTEGER,
            email          TEXT    UNIQUE NOT NULL,
            password_hash  TEXT    NOT NULL,
            availability   TEXT    DEFAULT 'Available',
            bio            TEXT
        )
    """)

    # ── Symptoms ───────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS symptoms (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,
            symptoms_json   TEXT,
            duration        TEXT,
            severity        TEXT,
            temperature     REAL,
            blood_pressure  TEXT,
            heart_rate      INTEGER,
            blood_sugar     REAL,
            additional_notes TEXT,
            report_file_path TEXT,
            created_at      DATETIME DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Predictions ────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id              INTEGER REFERENCES users(id) ON DELETE CASCADE,
            symptom_id           INTEGER REFERENCES symptoms(id) ON DELETE SET NULL,
            predicted_disease    TEXT,
            confidence           REAL,
            description          TEXT,
            precautions          TEXT,
            lifestyle            TEXT,
            foods_recommended    TEXT,
            foods_to_avoid       TEXT,
            exercise_recommendation TEXT,
            tablets              TEXT,
            report_file_path     TEXT,
            created_at           DATETIME DEFAULT (datetime('now','localtime'))
        )
    """)

    # Schema migration checks for existing DBs
    _ensure_column_exists(c, "symptoms", "report_file_path", "TEXT")
    _ensure_column_exists(c, "predictions", "tablets", "TEXT")
    _ensure_column_exists(c, "predictions", "report_file_path", "TEXT")

    # ── Messages ───────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id  INTEGER REFERENCES users(id)   ON DELETE CASCADE,
            doctor_id   INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
            sender_type TEXT    NOT NULL,   -- 'patient' or 'doctor'
            message     TEXT    NOT NULL,
            date_time   DATETIME DEFAULT (datetime('now','localtime')),
            read_status INTEGER  DEFAULT 0
        )
    """)

    # ── Appointments ───────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id       INTEGER REFERENCES users(id)   ON DELETE CASCADE,
            doctor_id        INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
            appointment_date TEXT,
            appointment_time TEXT,
            reason           TEXT,
            status           TEXT    DEFAULT 'Pending',
            created_at       DATETIME DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Ambulance Requests ──────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS ambulance_requests (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id          INTEGER REFERENCES users(id) ON DELETE SET NULL,
            patient_name     TEXT NOT NULL,
            patient_age      INTEGER,
            mobile_number    TEXT NOT NULL,
            area_location    TEXT NOT NULL,
            latitude         REAL,
            longitude        REAL,
            emergency_reason TEXT,
            maps_url         TEXT,
            status           TEXT DEFAULT 'Dispatched',
            ambulance_id     TEXT DEFAULT 'AMB-108',
            created_at       DATETIME DEFAULT (datetime('now','localtime'))
        )
    """)

    conn.commit()
    _seed_doctors(conn)
    conn.close()
    print("[OK] Database initialized successfully.")


def _ensure_column_exists(cursor, table, column, col_type):
    """Safely adds column to table if it doesn't exist already."""
    try:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        if column not in columns:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
    except Exception as e:
        print(f"[!] Column migration note ({table}.{column}): {e}")


def _seed_doctors(conn):
    """Insert sample doctors only if the table is empty."""
    from werkzeug.security import generate_password_hash

    c = conn.cursor()
    if c.execute("SELECT COUNT(*) FROM doctors").fetchone()[0] > 0:
        return  # Already seeded

    doctors = [
        ("Dr. Anil Kumar",    "General Medicine",  "MBBS, MD",          10, "dr.anil@healthapp.com",    "password123",
         "Available",  "Experienced general physician specializing in internal medicine and preventive care."),
        ("Dr. Priya Sharma",  "Cardiology",        "MBBS, MD, DM",      15, "dr.priya@healthapp.com",   "password123",
         "Available",  "Expert cardiologist with extensive experience in heart disease management."),
        ("Dr. Rahul Verma",   "Endocrinology",     "MBBS, MD, DNB",     12, "dr.rahul@healthapp.com",   "password123",
         "Available",  "Specialist in diabetes management, thyroid disorders, and hormonal conditions."),
        ("Dr. Sunita Patel",  "Pulmonology",       "MBBS, MD, FCCP",     8, "dr.sunita@healthapp.com",  "password123",
         "Available",  "Pulmonologist specializing in asthma, COPD, and respiratory disorders."),
        ("Dr. Vikram Singh",  "Neurology",         "MBBS, MD, DM",      20, "dr.vikram@healthapp.com",  "password123",
         "Busy",       "Senior neurologist specializing in migraines, epilepsy, and stroke management."),
        ("Dr. Meera Nair",    "Psychiatry",        "MBBS, MD Psychiatry",9, "dr.meera@healthapp.com",   "password123",
         "Available",  "Compassionate psychiatrist specializing in anxiety, depression, and stress management."),
        ("Dr. Karthik Rao",   "Infectious Disease","MBBS, MD, DTM&H",   11, "dr.karthik@healthapp.com", "password123",
         "Available",  "Infectious disease specialist experienced in dengue, malaria, typhoid, and COVID-19."),
    ]

    for d in doctors:
        name, spec, qual, exp, email, pwd, avail, bio = d
        hashed = generate_password_hash(pwd)
        c.execute(
            """INSERT OR IGNORE INTO doctors
               (name,specialization,qualification,experience,email,password_hash,availability,bio)
               VALUES (?,?,?,?,?,?,?,?)""",
            (name, spec, qual, exp, email, hashed, avail, bio)
        )
    conn.commit()
    print("[OK] Sample doctors seeded.")


# ── Convenience helpers ────────────────────────────────────────────────────

def query_one(sql, params=()):
    conn = get_db()
    row = conn.execute(sql, params).fetchone()
    conn.close()
    return row


def query_all(sql, params=()):
    conn = get_db()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def execute(sql, params=()):
    conn = get_db()
    c = conn.execute(sql, params)
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id


if __name__ == "__main__":
    init_db()
