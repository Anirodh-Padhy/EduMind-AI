import sqlite3

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

conn = sqlite3.connect(
    "edumind_ai.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ---------------------------------------------------
# USERS TABLE
# ---------------------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT,

    role TEXT DEFAULT 'student',

    approved INTEGER DEFAULT 0
)

""")

conn.commit() 

# ---------------------------------------------------
# COURSES TABLE
# ---------------------------------------------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS courses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    teacher TEXT,

    course_name TEXT,

    course_description TEXT
)

""")

conn.commit()