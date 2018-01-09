import psycopg2
import psycopg2.extensions
import psycopg2.extras
from datetime import date, datetime
from flask import g


# Connect to the database.
def connect_db():
    connection = psycopg2.connect("host=faraday.cse.taylor.edu port=5432 dbname=verbo user=verbo password=cuenca")
    dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # cursor = connection.cursor()
    g.connection = connection
    # print('connection = %s' % connection)
    # print('cursor = %s' % cursor)

    # TODO: Don't store the database password here.
    return dict_cur


def open_db_connection():
    """Open a connection to the database.
    Store the resulting connection in the `g.db` global object.
    """
    g.db = connect_db()


# If the database is open, close it.
def close_db_connection():
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


#################################### member ########################################


# creates a new member role
def create_user(member_id, password, role_id):
    query = '''
    INSERT INTO member_role(member_id, password, role_id, is_active)
    VALUES(%s, %s, %s, %s);
    '''
    g.db.execute(query, (member_id, password, role_id, '1'))
    #rowcount = g.db.rowcount
    g.connection.commit()
    return g.db.rowcount

# edits a member password
def update_user(member_id, password, role_id):
    query = '''
    UPDATE member_role SET  password = %s, role_id = %s
    WHERE member_id = %s
    '''
    g.db.execute(query,(password, role_id, member_id))
    g.connection.commit()
    return g.db.rowcount

# finds all roles
def find_roles():
    query='''
    SELECT * FROM role
    '''
    g.db.execute(query)
    return g.db.fetchall()

# finds all the members and their roles
def get_all_member_roles():
    query = '''
    select first_name, last_name, member.id, homegroup_id, role_id, role, member_role.is_active as "roleActive", homegroup_leader.is_active as "hgLeaderActive", name as "hgName" from member 
    left outer join member_role on member.id = member_role.member_id 
    left outer join homegroup_leader on member.id = homegroup_leader.member_id
    left outer join role on member_role.role_id = role.id 
    left outer join homegroup on homegroup_leader.homegroup_id = homegroup.id
    where member.is_active = '1'
    order by last_name, first_name
    '''
    g.db.execute(query)
    return g.db.fetchall()

# finds member based on an email
def find_user(email):
    g.db.execute('SELECT * from member join member_role on member.id = member_role.member_id join role on member_role.role_id = role.id WHERE member.email = %s', (email,))
    return g.db.fetchone()

def find_user_info(id):
    g.db.execute('SELECT * from member join member_role on member_role.member_id = member.id WHERE member.id =%s', (id,))
    return g.db.fetchone()

# finds if the user is active
def role_is_active(id, role_id):
    g.db.execute('select is_active from member_role where member_id = %s and role_id = %s', (id, role_id))
    return g.db.fetchone()

# finds if the user has an active role
def has_active_role (id):
    g.db.execute('''select is_active from member_role where member_id = %s and is_active = '1' ''', id)
    return g.db.fetchone()

# updates the user role
def update_role(id, role_id, is_active):
    query = '''
        UPDATE member_role SET is_active = %s
        where member_id = %s and role_id = %s
        '''
    g.db.execute(query, ( is_active,id, role_id))
    g.connection.commit()
    return g.db.rowcount


# updates the user role from admin role view based on selection
def assign_new_role(id, role_id):
    query = '''
    update member_role set is_active = '1', role_id = %s where member_id = %s
    '''
    g.db.execute(query, ( role_id, id ))
    g.connection.commit()
    return g.db.rowcount


# finds the most recent member entered into the db
def recent_user():
    g.db.execute('select id from member order by id desc LIMIT 1')
    return g.db.fetchone()

# grabs all members in the db
def get_all_users():
    query = '''
        SELECT * FROM member_role
      JOIN role on member_role.role_id = role.id
      JOIN member on member.id = member_role.member_id
        '''
    g.db.execute(query)
    return g.db.fetchall()

# finds a members associated homegroup (specifically for homegroup leaders)
def find_user_homegroup(email):

    g.db.execute('SELECT * from homegroup_leader JOIN member on homegroup_leader.member_id = member.id WHERE email = %s',(email,))
    return g.db.fetchone()['homegroup_id']

# finds the most recent member entered into the db
def recent_user():
    g.db.execute('select id from member order by id desc LIMIT 1')
    return g.db.fetchone()

#################################### MEMBER ########################################

# returns a count of all members in the db
def get_member_count():
    query = '''
        SELECT count(id)
        FROM member
        '''
    return g.db.execute(query).fetchall()

# finds member info by passing in an email
def find_member_info(email):
    g.db.execute('SELECT * from member WHERE email =%s', (email,))
    return g.db.fetchone()

# finds member info by passing in a member id
def find_member(member_id):
    g.db.execute('SELECT * FROM member WHERE id = %s', (member_id,))
    return g.db.fetchone()

# finds all members in the db
def get_all_members():
    query = '''
    SELECT * FROM member
    WHERE is_active='1'
    ORDER BY last_name asc
    '''
    g.db.execute(query)
    return add_age_to_member_rows(g.db.fetchall())

def add_age_to_member_rows(rows):
    resultSet = []
    for row in rows:
        member = {}
        for field in row.keys():
            member[field] = row[field]
        member["age"] = int((date.today() - datetime.strptime(member["birthday"], '%Y-%m-%d').date()).days / 365.25)
        resultSet.append(member)
    return resultSet

# finds all members NOT in a particular homegroup
def get_all_members_not_in_homegroup(homegroup_id):
    homegroup_id = int (homegroup_id)
    query ='''
    select * from member where member.is_active = '1' and member.id not in (
    select member_id from homegroup_member
    where homegroup_id = :%s and
    homegroup_member.is_active = '1'
    )
    '''
    g.db.execute(query, ( homegroup_id))
    return g.db.fetchall()

# finds all the inactive homegroup members
def get_homegroup_inactive_members(homegroup_id):
    return g.db.execute('''SELECT * FROM member
        JOIN homegroup_member ON member.id = homegroup_member.member_id
        JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
        WHERE homegroup_member.is_active != '1' and  homegroup.id = %s''', (homegroup_id,)).fetchall()


# sets a homegroup member to be reactivated in the homegroup
def reactive_homegroup_member(homegroup_id, member_id):

    query = '''
    UPDATE homegroup_member SET is_active = '1'
    where homegroup_id = %s and member_id = %s
    '''
    g.db.execute(query, (homegroup_id, member_id))
    g.connection.commit()
    return g.db

# finds all inactive members in the db
def get_all_inactive_members():
    query = '''
    SELECT * FROM member
    WHERE is_active='0'
    '''
    g.db.execute(query)
    return add_age_to_member_rows(g.db.fetchall())

# edits member info
def edit_member(member_id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status, join_date):
    member_id = int(member_id)

    query = '''
    UPDATE member SET first_name = %s, last_name = %s, email = %s, phone_number = %s, gender = %s, birthday = %s, baptism_status = %s, marital_status = %s, join_date = %s
    WHERE id = %s
    '''
    g.db.execute(query, (first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status, join_date, member_id))
    g.connection.commit()
    return g.db.rowcount


# creates a new member
def create_member(first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status, join_date):
    query = '''
    INSERT INTO member(first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status, join_date, is_active)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, '1')
    '''
    g.db.execute(query, (first_name,  last_name, email, phone_number,  gender,  birthday,
                                   baptism_status,  marital_status,  join_date))
    g.connection.commit()


    return g.db.rowcount


# adds leader to a homegroup
def add_leader_to_homegroup(member_id, homegroup_id):
    g.db.execute('select * from homegroup_leader where member_id =%s ', (member_id))
    if (g.db.fetchone()):
        g.db = connect_db()
        query = '''update homegroup_leader set is_active = '1', homegroup_id = %s where member_id = %s'''
        g.db.execute(query, ( homegroup_id, member_id))
    else:
        g.db = connect_db()
        query = '''
        INSERT INTO homegroup_leader(member_id, homegroup_id, is_active) values(%s, %s, '1')
        '''
        g.db.execute(query, (member_id, homegroup_id))
    g.connection.commit()
    return g.db.rowcount




# deactivates hg leader

def deactivate_hgleader(member_id, homegroup_id):
    query = '''
    update  homegroup_leader set is_active = '0'
    where member_id = %s and homegroup_id = %s
    '''
    g.db.execute(query, (member_id, homegroup_id))
    g.connection.commit()
    g.db = connect_db()
    query = '''
    update member_role set is_active = '0'
    where member_id = %s '''
    g.db.execute(query, (member_id))
    return g.db.rowcount



# adds a member to a homegroup
def add_member_to_homegroup(homegroup_id, member_id):
    homegroup_id = int(homegroup_id)
    member_id = int(member_id)
    query = '''
    INSERT INTO homegroup_member values(%s, %s, '1')
    '''
    g.db.execute(query, ( homegroup_id, member_id))
    g.db.commit()
    return g.db.rowcount

# finds the most recent member entered into the db
def recent_member():
    g.db.execute('select id from member order by id desc LIMIT 1')
    return g.db.fetchone()

# removes a member from a homegroup -- really just sets them inactive
def remove_member(homegroup_id, member_id):
    member_id = int(member_id)
    homegroup_id = int(homegroup_id)
    query = '''
    UPDATE homegroup_member SET is_active = '0'
    WHERE homegroup_id = %s AND member_id = %s
    '''
    g.db.execute(query, (homegroup_id,  member_id))
    g.db.commit()
    return g.db.rowcount

# this sets a member as inactive in the system
def deactivate_member(member_id):
    query='''
    UPDATE member SET is_active = '0'
    WHERE id = %s
    '''
    g.db.execute(query, ( member_id))
    g.connection.commit()
    return g.db

# this sets a member as active in the system
def reactivate_member(member_id):
    query='''
    UPDATE member SET is_active = '1'
    WHERE id = %s
    '''
    g.db.execute(query, member_id)
    g.connection.commit()
    return g.db

# finds all members in a particular homegroup
def get_homegroup_members(homegroup_id):
    query = '''
        SELECT * FROM member
        JOIN homegroup_member ON member.id = homegroup_member.member_id
        JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
        WHERE homegroup_member.is_active = '1' and  homegroup.id = %s
    '''
    g.db.execute(query, (homegroup_id,))
    return g.db.fetchall()

def get_homegroup_emails(homegroup_id):
    return g.db.execute('''SELECT email FROM member
        JOIN homegroup_member ON member.id = homegroup_member.member_id
        JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
        WHERE homegroup_member.is_active = '1' and  homegroup.id = %s''', (homegroup_id,)).fetchall()

# finds if a member has missed (number_of_misses) consecutive meetings
def system_attendance_alert(homegroup_id, member_id, number_of_misses):
    query = """
    SELECT  * FROM attendance
    WHERE homegroup_id = %s and member_id = %s
    ORDER BY meeting_id desc
    LIMIT %s
    """
    g.db.execute(query, (homegroup_id, member_id, number_of_misses))
    return g.db.fetchall()


#################################### HOME GROUP ########################################



# finds a homegroup leader
def find_homegroup_leader(homegroup_id):
    homegroup_id = int(homegroup_id)
    return g.db.execute('''
    SELECT * from homegroup_leader join member on member.id = homegroup_leader.member_id
    join homegroup_id = homegroup.id
    where homegroup_id = %s
    ''', (homegroup_id,)).fetchone()


# finds a member's homegroup
def find_member_homegroup(member_id):
    member_id = int(member_id)
    return g.db.execute('''
    SELECT * from homegroup_member join member on member.id = homegroup_member.member_id
    where member_id = %s
    ''', (member_id,)).fetchone()




# finds all the attendance dates entered in a particular homegroup
def get_attendance_dates(homegroup_id):
    homegroup_id = int(homegroup_id)

    query = '''
        SELECT DISTINCT meeting.date, meeting.time, attendance.meeting_id
        from meeting JOIN attendance on meeting.id = attendance.meeting_id
        WHERE homegroup_id = %s
    '''
    g.db.execute(query, (homegroup_id,))
    return g.db.fetchall()


# creates a new attendance report and initializes everyones attendance to false
def generate_attendance_report(homegroup_id, meeting_id):
    members = get_homegroup_members(homegroup_id)
    for member in members:
        print (member)
        query = '''INSERT INTO attendance (homegroup_id, member_id, meeting_id, attendance)
        VALUES (%s, %s, %s, %s)
        '''
        g.db.execute(query, ( homegroup_id, member['member_id'], meeting_id, '0'))
    g.connection.commit()
    return g.db.rowcount

# returns the attendance of a particular homegroup on a particular day/time
def get_attendance(homegroup_id, meeting_id):
    meeting_id = int(meeting_id)
    query = '''SELECT * from attendance join member on attendance.member_id = member.id
                WHERE homegroup_id = %s and meeting_id = %s '''
    g.db.execute(query, (homegroup_id, meeting_id))
    return g.db.fetchall()


# finds date information from a meeting id
def find_date(meeting_id):
    g.db.execute('SELECT * from meeting WHERE id =%s', (meeting_id,))
    return g.db.fetchone()

# updates attendance for a homegroup's member on a particular day/time
def update_attendance(homegroup_id, member_id, meeting_id, attendance):
    query = '''
        UPDATE attendance SET attendance = %s
        WHERE homegroup_id = %s and member_id = %s and meeting_id = %s
        '''
    g.db.execute(query, (attendance, homegroup_id,  member_id, meeting_id))
    g.connection.commit()
    return g.db.rowcount

# creates a new date or "meeting" time in the db
def add_date(date, time):
    query = '''
    INSERT INTO meeting (date, time) VALUES (%s, %s)
    '''
    g.db.execute(query, (date, time))
    g.connection.commit()
    g.db = connect_db()
    query = '''SELECT id from meeting order by id desc limit 1'''
    g.db.execute(query)
    return g.db.fetchone()

# returns the most recent homegroup added to the db
def recent_homegroup():
    g.db.execute('select id from homegroup order by id desc LIMIT 1')
    return g.db.fetchone()

# finds a homegroup based on homegroup_id
def find_homegroup(homegroup_id):
    g.db.execute('SELECT * from homegroup WHERE id =%s', (homegroup_id,))
    return g.db.fetchone()

# creates a new homegroup
def create_homegroup(name, location, description, latitude, longitude):
    query = '''
        INSERT INTO homegroup(name, location, description, latitude, longitude, is_active)
        VALUES(%s, %s, %s, %s, %s, '1')
        '''
    g.db.execute(query, ( name, location, description, latitude, longitude))
    g.connection.commit()
    return g.db.rowcount

# edits homegroup info
def edit_homegroup(homegroup_id, name, location, description, latitude, longitude):
    query = '''
    UPDATE homegroup SET name = %s, location = %s, description = %s, latitude = %s, longitude = %s
    WHERE id = %s
    '''
    g.db.execute(query,  (name,  location,
                                  description, latitude,  longitude, homegroup_id))
    g.connection.commit()
    return g.db.rowcount

# returns all homegroups
def get_all_homegroups():
    query = '''
        SELECT * FROM homegroup
        WHERE is_active='1'
        '''
    g.db.execute(query)
    return g.db.fetchall()

# returns all homegroup info - including leader info etc.
def get_all_homegroup_info():
    query = '''
        select * from homegroup left outer join homegroup_leader on homegroup.id = homegroup_leader.homegroup_id left outer join member on homegroup_leader.member_id = member.id
    '''
    g.db.execute(query)
    return g.db.fetchall()


# deactivates a homegroup
def deactivate_homegroup(homegroup_id):
    query='''
    UPDATE homegroup SET is_active = '0'
    WHERE id = %s
    '''
    g.db.execute(query, ( homegroup_id))
    g.connection.commit()
    return g.db.rowcount

def reactivate_homegroup(homegroup_id):
    query='''
    UPDATE homegroup SET is_active = '1'
    WHERE id = %s
    '''
    g.db.execute(query, ( homegroup_id))
    g.connection.commit()
    return g.db.rowcount

def get_all_inactive_homegroups():
    query = '''
    SELECT * FROM homegroup
    WHERE is_active='0'
    '''
    g.db.execute(query)
    return g.db.fetchall()

#################################### Admin ########################################

# finds all active admin in the db
def get_all_admin():
    query = '''
        SELECT * FROM member
        JOIN member_role ON member.id = member_role.member_id
        JOIN role ON member_role.role_id = role.id
        WHERE role.role="admin" AND member_role.is_active = '1' AND member.is_active = '1'
        '''
    g.db.execute(query)
    return g.db.fetchall()

# finds all inactive admin in the db
def get_all_inactive_admin():
    query = '''
    SELECT * FROM member
     JOIN member_role ON member.id = member_role.member_id
        JOIN role ON member_role.role_id = role.id
    WHERE role.role="admin" AND member_role.is_active = '0' AND member.is_active = '0'
    '''
    g.db.execute(query)
    return g.db.fetchall()

def get_attendance_counts():
    query = '''
    SELECT date, time, COUNT(member.id) AS "countMembers" FROM attendance
    JOIN meeting ON attendance.meeting_id = meeting.id
    JOIN member ON attendance.member_id = member.id
    WHERE attendance = '1'
    GROUP BY date, time
    '''
    g.db.execute(query)
    return g.db.fetchall()

def get_homegroup_attendance_counts(myhomegroup):
    query = '''
    SELECT date, time, meeting_id, COUNT(member.id) AS "countMembers" FROM attendance
    JOIN meeting ON attendance.meeting_id = meeting.id
    JOIN member ON attendance.member_id = member.id
    WHERE attendance = '1' AND homegroup_id = %s
    GROUP BY date, time, meeting_id, member_id
    '''
    g.db.execute(query, myhomegroup)
    return g.db.fetchall()

def get_all_members_emails():
    query = '''
    SELECT email
    FROM member
    '''
    g.db.execute(query)
    return g.db.fetchall()

def get_homegroup_emails(homegroup_id):
    query = '''
    SELECT email FROM member
        JOIN homegroup_member ON member.id = homegroup_member.member_id
        JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
    WHERE homegroup_id = %s'''
    g.db.execute(query, (homegroup_id))
    return g.db.fetchall()