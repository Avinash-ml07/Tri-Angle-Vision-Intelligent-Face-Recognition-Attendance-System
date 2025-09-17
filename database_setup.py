import sqlite3

def init_face_db():
    """Initialize the faces database"""
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS faces (
                    name TEXT,
                    encoding BLOB)''')
    conn.commit()
    conn.close()
    print("Faces database initialized successfully.")

def init_attendance_db():
    """Initialize the attendance database"""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    name TEXT,
                    date TEXT,
                    time TEXT)''')
    conn.commit()
    conn.close()
    print("Attendance database initialized successfully.")

def initialize_databases():
    """Initialize both databases"""
    init_face_db()
    init_attendance_db()

if __name__ == "__main__":
    initialize_databases()