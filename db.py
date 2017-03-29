import sqlite3
import os
from flask import g

# from application import app
DATABASE = 'MyDatabase.sqlite'

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

def get_users():
    query = '''
        SELECT user.first_name, user.last_name
        FROM user
        '''
    return g.db.execute(query).fetchall()

def get_user_count():
    query = '''
        SELECT count(id)
        FROM user
        '''
    return g.db.execute(query).fetchall()

def get_dates():
    query='''
        SELECT
    '''
def add_attendance(user_id, meeting_id, attendance):
    query = '''
        INSERT INTO attendance (user_id, meeting_id, attendance)
        VALUES ( :user_id, :meeting_id, :attendance );
        '''
    cursor = g.db.execute(query, {'User Id': user_id, 'Attendance': attendance, 'Meeting Id': meeting_id})
    g.db.commit()
    return cursor.rowcount
    # return
    #g.db.execute(query).fetchall()

def create_user(first_name, last_name, email):
    query = '''
    INSERT INTO user(first_name, last_name, email)
    VALUES(:first_name, :last_name, :email)
    '''
    cursor = g.db.execute(query, {'first_name': first_name, 'last_name': last_name, 'email':email})
    g.db.commit()
    return cursor.rowcount

def get_all_users():
    cursor = g.db.execute('select * from user')
    return cursor.fetchall()


def find_user(user_id):
    return g.db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

def edit_user(user_id, first_name, last_name, email):
    query = '''
    UPDATE user SET first_name = :first, last_name = :last, email = :email
    WHERE id = :user_id
    '''
    cursor = g.db.execute(query, {'user_id': user_id, 'first': first_name, 'last': last_name, 'email': email})
    g.db.commit()
    return cursor.rowcount