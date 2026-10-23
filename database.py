import sqlite3

def create_database():
    conn = sqlite3.connect("campus_booking.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    campus_id INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS campuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    max_duration INTEGER NOT NULL,
    restricted_hours TEXT
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            campus_id INTEGER NOT NULL,
            UNIQUE(name, campus_id),
            FOREIGN KEY (campus_id) REFERENCES campuses(id)
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    campus_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    duration INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (resource_id) REFERENCES resources(id),
    FOREIGN KEY (campus_id) REFERENCES campuses(id)
    )
    ''')
    cursor.execute("SELECT COUNT(*) FROM campuses")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO campuses (name, max_duration, restricted_hours) VALUES ('Campus A', 2, '08:00-18:00')")
        cursor.execute("INSERT INTO campuses (name, max_duration, restricted_hours) VALUES ('Campus B', 4, '08:00-20:00')")
        cursor.execute("INSERT INTO campuses (name, max_duration, restricted_hours) VALUES ('Campus C', 1, '08:00-16:00')")

    conn.commit()
    conn.close()
    print("Database created successfully.")

if __name__ == "__main__":
    create_database()