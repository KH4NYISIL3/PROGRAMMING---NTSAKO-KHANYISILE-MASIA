import sqlite3
from datetime import datetime, timedelta
from campus_roles import SystemUser, AcademicStaff, CampusManager, GlobalOperator


def get_db_connection():
    conn = sqlite3.connect('campus_booking.db')
    conn.row_factory = sqlite3.Row
    return conn


def register_user(username, password, role, campus_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Auto-fix role names so they match the system
    r_lower = role.lower()
    if "admin" in r_lower:
        role = "CampusAdmin"
    elif "operator" in r_lower:
        role = "SystemOperator"
    elif "lecturer" in r_lower:
        role = "Lecturer"

    try:
        cursor.execute('''
            INSERT INTO users (username, password, role, campus_id)
            VALUES (?, ?, ?, ?)
        ''', (username, password, role, campus_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password))

    row = cursor.fetchone()
    conn.close()

    if row:
        role_in_db = row['role']

        if "admin" in role_in_db.lower():
            return CampusManager(row['id'], row['username'], row['password'], row['campus_id'])
        elif "operator" in role_in_db.lower():
            return GlobalOperator(row['id'], row['username'], row['password'])
        elif "lecturer" in role_in_db.lower():
            return AcademicStaff(row['id'], row['username'], row['password'], row['campus_id'])
        else:
            return SystemUser(row['id'], row['username'], row['password'], role_in_db, row['campus_id'])
    else:
        return None


def check_booking_rules(campus_id, resource_id, date, start_time, duration):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT max_duration, name FROM campuses WHERE id = ?", (campus_id,))
    campus = cursor.fetchone()

    if not campus:
        conn.close()
        return False, "Campus not found."

    if duration > campus['max_duration']:
        conn.close()
        return False, f"Policy Violation: {campus['name']} allows a maximum of {campus['max_duration']} hours."

    cursor.execute('''
        SELECT date, start_time, duration FROM bookings 
        WHERE resource_id = ? AND date = ?
    ''', (resource_id, date))
    existing_bookings = cursor.fetchall()

    try:
        new_start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        new_end = new_start + timedelta(hours=duration)
    except ValueError:
        conn.close()
        return False, "Invalid date or time format. Use YYYY-MM-DD and HH:MM."

    for booking in existing_bookings:
        try:
            ex_start = datetime.strptime(f"{booking['date']} {booking['start_time']}", "%Y-%m-%d %H:%M")
            ex_end = ex_start + timedelta(hours=booking['duration'])

            if (new_start < ex_end) and (new_end > ex_start):
                conn.close()
                return False, f"Double Booking! This resource is already booked from {booking['start_time']}."
        except ValueError:
            continue

    conn.close()
    return True, "Valid"

def create_booking(user, resource_id, date, start_time, duration):
    campus_id = user.campus_id

    valid, message = check_booking_rules(
        campus_id, resource_id, date, start_time, duration
    )

    if not valid:
        return False, message

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO bookings
            (user_id, resource_id, campus_id, date, start_time, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user.user_id, resource_id, campus_id,
            date, start_time, duration
        ))

        conn.commit()
        return True, "Booking created successfully."

    except sqlite3.Error as e:
        return False, f"Database error: {e}"

    finally:
        conn.close()