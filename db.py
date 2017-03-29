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

def create_user(first_name, last_name, email, phone_number, gender, birthday, baptism_status, join_date):
    query = '''
    INSERT INTO user(first_name, last_name, email, phone_number, gender, birthday, baptism_status, join_date)
    VALUES(:first_name, :last_name, :email, :phone_number, :gender, :birthday, :baptism_status, :join_date)
    '''
    cursor = g.db.execute(query, {'first_name': first_name, 'last_name': last_name, 'email':email, 'phone_number':phone_number, 'gender':gender, 'birthday':birthday, 'baptism_status':baptism_status, 'join_date':join_date})
    g.db.commit()
    return cursor.rowcount

def add_user_to_homegroup(homegroup_id, user_id):
    query = '''
    INSERT INTO homegroup_user values(:homegroup_id, :user_id)
    '''
    cursor = g.db.execute(query, {'homegroup_id': homegroup_id, 'user_id': user_id})
    g.db.commit()
    return cursor.rowcount



def recent_user():
    cursor = g.db.execute('select id from user order by id desc LIMIT 1')
    return cursor.fetchone()

def get_all_users():
    cursor = g.db.execute('select * from user')
    return cursor.fetchall()


def find_user(user_id):
    return g.db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

def edit_user(user_id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, join_date):
    query = '''
    UPDATE user SET first_name = :first, last_name = :last, email = :email, phone_number = :phone, gender = :gender, birthday = :bday, baptism_status = :baptism, join_date = :join
    WHERE id = :user_id
    '''
    cursor = g.db.execute(query, {'user_id': user_id, 'first': first_name, 'last': last_name, 'email': email, 'phone': phone_number, 'gender': gender, 'bday': birthday, 'baptism': baptism_status, 'join': join_date })
    g.db.commit()
    return cursor.rowcount


def find_homegroup(homegroup_id):
    return g.db.execute('SELECT * from homegroup WHERE id =?', (homegroup_id,)).fetchone()



def edit_homegroup(homegroup_id, name, location, description):
    query = '''
    UPDATE homegroup SET name = :name, location = :location, description = :description
    WHERE id = :homegroup_id
    '''
    cursor = g.db.execute(query, {'homegroup_id': homegroup_id, 'name': name, 'location': location, 'description': description})
    g.db.commit()
    return cursor.rowcount



def get_homegroup_users(homegroupid):
    return g.db.execute('''SELECT * FROM user
    JOIN homegroup_user ON user.id = homegroup_user.user_id
    JOIN homegroup ON homegroup_user.homegroup_id = homegroup.id
    WHERE homegroup.id = ?''', (homegroupid,)).fetchall()