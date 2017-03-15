import sqlite3
import os
from flask import g

# from application import app
DATABASE = ''

# Connect to the database.
def connect_db(db_path):
    if db_path is None:
      db_path = os.path.join(os.getcwd(), DATABASE)
    if not os.path.isfile(db_path):
        raise RuntimeError("Can't find database file '{}'".format(db_path))
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection

def open_db_connection(db_path=None):
    """Open a connection to the database.
    Open a connection to the SQLite database at `db_path`.
    Store the resulting connection in the `g.db` global object.
    """
    g.db = connect_db(db_path)


# If the database is open, close it.
def close_db_connection():
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# creates a page containing the details of all trips
def create_trip_report():
    query = '''
    SELECT student.first_name, student.last_name,
    student.year, trip.destination, trip.trip_year, trip.semester
    FROM student INNER JOIN student_trip ON student.id = student_trip.student_id
    INNER JOIN trip ON student_trip.trip_id = trip.id
    '''
    return g.db.execute(query).fetchall()

def add_attendance(user_id, attendance):
    query = '''
        INSERT INTO trip (user_id, attendance, trip_year)
        VALUES ( :destination, :semester, :trip_year );
        '''
    cursor = g.db.execute(query, {'User Id': user_id, 'Attendance': attendance})
    g.db.commit();
    return cursor.rowcount
    # return g.db.execute(query).fetchall()