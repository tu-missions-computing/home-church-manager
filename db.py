import psycopg2
import psycopg2.extensions
import psycopg2.extras
from datetime import date, datetime
from flask import g

from psql_settings import data_source


def open_db_connection():
    """Open connection to database."""
    g.connection = psycopg2.connect(**data_source)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def close_db_connection():
    """Close connection to the database."""
    g.cursor.close()
    g.connection.close()


# Member ########################################

def calculate_age(born):
    """Return a person's age"""
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def create_member_role(member_id, password, role_id):
    """Assign a member to the given role"""
    query = '''
    INSERT INTO member_role(member_id, password, role_id, is_active)
    VALUES(%(member_id)s, %(password)s, %(role_id)s, TRUE);
    '''
    g.cursor.execute(query, {'member_id': member_id, 'password': password, 'role_id': role_id})
    g.connection.commit()
    return g.cursor.rowcount


def update_password(member_id, password, role_id):
    query = '''
    UPDATE member_role SET  password = %s, role_id = %s
    WHERE member_id = %s
    '''
    g.cursor.execute(query, (password, role_id, member_id))
    g.connection.commit()
    return g.cursor.rowcount


def get_all_roles():
    g.cursor.execute('SELECT * FROM role')
    return g.cursor.fetchall()


def find_member_role(member_id):
    """Get the role for this member, if any (may return None)"""
    query = """
    SELECT * 
    FROM member_role 
    WHERE member_role.member_id = %(member_id)s"""
    g.cursor.execute(query, {'member_id': member_id})
    return g.cursor.fetchone()


# finds all the members and their roles
def get_all_member_roles():
    query = '''
    SELECT first_name, last_name, member.id, homegroup_id, role_id, role, member_role.is_active AS "roleActive", homegroup_leader.is_active AS "hgLeaderActive", name AS "hgName" FROM member 
    LEFT OUTER JOIN member_role ON member.id = member_role.member_id 
    LEFT OUTER JOIN homegroup_leader ON member.id = homegroup_leader.member_id
    LEFT OUTER JOIN role ON member_role.role_id = role.id 
    LEFT OUTER JOIN homegroup ON homegroup_leader.homegroup_id = homegroup.id
    WHERE member.is_active = TRUE
    ORDER BY last_name, first_name
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


# finds member based on an email
def find_user(email):
    query = """
SELECT member.id, member_role.member_id,
  first_name, last_name, email, phone_number, gender, birthday,
  baptism_status, marital_status_id, how_did_you_find_out_id,
  is_a_parent, join_date, member.is_active,
  password, role_id, role
FROM member
  JOIN member_role ON member.id = member_role.member_id
  JOIN role ON member_role.role_id = role.id
WHERE member.email = %(email)s AND member_role.is_active = TRUE
    """
    g.cursor.execute(query, {'email': email})
    return g.cursor.fetchone()


def find_user_info(id):
    g.cursor.execute('SELECT * FROM member JOIN member_role ON member_role.member_id = member.id WHERE member.id =%s',
                     (id,))
    return g.cursor.fetchone()


# finds if the user is active
def is_role_active(id, role_id):
    g.cursor.execute('SELECT is_active FROM member_role WHERE member_id = %s AND role_id = %s', (id, role_id))
    return g.cursor.fetchone()


# finds if the user has an active role
def has_active_role(id):
    g.cursor.execute('''SELECT is_active FROM member_role WHERE member_id = %s AND is_active = TRUE ''', (id,))
    return g.cursor.fetchone()


# updates the user role
def update_role(id, role_id, is_active):
    query = '''
        UPDATE member_role SET is_active = %s
        WHERE member_id = %s AND role_id = %s
        '''
    g.cursor.execute(query, (is_active, id, role_id))
    g.connection.commit()
    return g.cursor.rowcount


def get_all_marital_statuses():
    # Get all the marital status values.
    g.cursor.execute('SELECT * FROM marital_status')
    return g.cursor.fetchall()


def get_marital_status_by_name(name):
    g.cursor.execute('SELECT * FROM marital_status WHERE marital_status_name=%(name)s', {'name': name})
    return g.cursor.fetchone()


# retrieves all the methods of finding out about the homegroups/church
def get_all_how_did_you_find_out_values():
    g.cursor.execute('SELECT * FROM how_did_you_find_out ')
    return g.cursor.fetchall()


def get_how_did_you_find_out_by_name(name):
    g.cursor.execute('SELECT * FROM how_did_you_find_out WHERE how_did_you_find_out_name=%(name)s', {'name': name})
    return g.cursor.fetchone()


# updates the user role from admin role view based on selection
def assign_new_role(id, role_id):
    query = '''
    UPDATE member_role SET is_active = TRUE, role_id = %s WHERE member_id = %s
    '''
    g.cursor.execute(query, (role_id, id))
    g.connection.commit()
    return g.cursor.rowcount


# finds the most recent member entered into the db
def recent_user():
    g.cursor.execute('SELECT id FROM member ORDER BY id DESC LIMIT 1')
    return g.cursor.fetchone()


# grabs all members in the db
def get_all_users():
    query = '''
        SELECT * FROM member_role
      JOIN role ON member_role.role_id = role.id
      JOIN member ON member.id = member_role.member_id
        '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


# finds a members associated homegroup (specifically for homegroup leaders)
def find_user_homegroup(email):
    g.cursor.execute(
        'SELECT * FROM homegroup_leader JOIN member ON homegroup_leader.member_id = member.id WHERE email = %s',
        (email,))
    return g.cursor.fetchone()['homegroup_id']


# MEMBER ########################################


def find_member_info(email):
    """Find member by email."""
    g.cursor.execute('SELECT * FROM member WHERE email = %(email)s', {'email': email})
    return g.cursor.fetchone()


def find_member(member_id):
    """Find member by ID."""
    g.cursor.execute('SELECT * FROM member WHERE id = %(id)s', {'id': member_id})
    return g.cursor.fetchone()


def get_all_members():
    """Get all active members."""
    query = '''
    SELECT * FROM member
    WHERE is_active=TRUE
    ORDER BY last_name ASC
    '''
    g.cursor.execute(query)
    return add_age_to_member_rows(g.cursor.fetchall())


def add_age_to_member_rows(rows):
    result_set = []
    for row in rows:
        member = {}
        for field in row.keys():
            member[field] = row[field]
        member["age"] = int((date.today() - datetime.strptime(member["birthday"], '%Y-%m-%d').date()).days / 365.25)
        result_set.append(member)
    return result_set


def get_all_members_not_in_homegroup(homegroup_id):
    """Find all members NOT in a particular homegroup."""
    query = """
    SELECT *
    FROM member
    WHERE member.is_active = TRUE AND member.id NOT IN (
      SELECT member_id
      FROM homegroup_member
      WHERE homegroup_id = %s AND
            homegroup_member.is_active = TRUE
    )
    """
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


# finds all the inactive homegroup members
def get_homegroup_inactive_members(homegroup_id):
    g.cursor.execute('''SELECT * FROM member
            JOIN homegroup_member ON member.id = homegroup_member.member_id
            JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
            WHERE homegroup_member.is_active != TRUE AND  homegroup.id = %s
            ORDER BY last_name, first_name''', (homegroup_id,))
    return g.cursor.fetchall()


# sets a homegroup member to be reactivated in the homegroup
def reactive_homegroup_member(homegroup_id, member_id):
    query = '''
    UPDATE homegroup_member SET is_active = TRUE
    WHERE homegroup_id = %s AND member_id = %s
    '''
    g.cursor.execute(query, (homegroup_id, member_id))
    g.connection.commit()
    return g.cursor.rowcount


# finds all inactive members in the db
def get_all_inactive_members():
    query = '''
    SELECT * FROM member
    WHERE is_active=FALSE
    ORDER BY last_name, first_name
    '''
    g.cursor.execute(query)
    return add_age_to_member_rows(g.cursor.fetchall())


# edits member info
def edit_member(member_info):
    query = '''
    UPDATE member SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, 
      phone_number = %(phone_number)s, gender = %(gender)s, birthday = %(birthday)s, 
      baptism_status = %(baptism_status)s, 
      marital_status_id = %(marital_status_id)s, how_did_you_find_out_id = %(how_did_you_find_out_id)s, 
      is_a_parent = %(is_a_parent)s, join_date = %(join_date)s, is_active = %(is_active)s
    WHERE id = %(id)s
    '''
    g.cursor.execute(query, member_info)
    g.connection.commit()
    return g.cursor.rowcount


def create_member(member_info):
    """Create a new member."""
    query = '''
    INSERT INTO member(first_name, last_name, email, phone_number, gender, birthday, 
        baptism_status, marital_status_id, how_did_you_find_out_id, is_a_parent, join_date, is_active)
    VALUES(%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(gender)s, %(birthday)s, 
        %(baptism_status)s, %(marital_status_id)s, %(how_did_you_find_out_id)s, %(is_a_parent)s, %(join_date)s, TRUE)
    RETURNING id
    '''
    g.cursor.execute(query, member_info)
    g.connection.commit()
    return {'id': g.cursor.fetchone()['id'], 'rowcount': g.cursor.rowcount}


# adds leader to a homegroup
def add_leader_to_homegroup(member_id, homegroup_id):
    g.cursor.execute('SELECT * FROM homegroup_leader WHERE member_id =%s ', (member_id,))
    if g.cursor.fetchone():
        query = '''UPDATE homegroup_leader SET is_active = TRUE, homegroup_id = %s WHERE member_id = %s'''
        g.cursor.execute(query, (homegroup_id, member_id))
    else:
        query = '''
        INSERT INTO homegroup_leader(member_id, homegroup_id, is_active) VALUES(%s, %s, TRUE)
        '''
        g.cursor.execute(query, (member_id, homegroup_id))
    g.connection.commit()
    return g.cursor.rowcount


def deactivate_hgleader(member_id, homegroup_id):
    """Deactivate home group leader."""
    query = '''
    UPDATE  homegroup_leader SET is_active = FALSE
    WHERE member_id = %s AND homegroup_id = %s
    '''
    g.cursor.execute(query, (member_id, homegroup_id))
    g.connection.commit()
    deactivate_hgleader_role(member_id)
    return g.cursor.rowcount


def deactivate_hgleader_role(member_id):
    query = '''
        UPDATE member_role SET is_active = FALSE
        WHERE member_id = %s '''
    g.cursor.execute(query, (member_id,))
    g.connection.commit()
    return g.cursor.rowcount


# adds a member to a homegroup
def add_member_to_homegroup(homegroup_id, member_id):
    # The member may already be associated with the homegroup - just marked inactive.
    query = '''
        UPDATE homegroup_member SET is_active = TRUE
        WHERE homegroup_id = %s AND member_id = %s
        '''
    g.cursor.execute(query, (homegroup_id, member_id))
    g.connection.commit()
    if g.cursor.rowcount == 0:
        # The member is not already associated with the homegroup - insert a new association record
        now = datetime.now()
        date = now.strftime("%m-%d-%Y")
        query = '''
        INSERT INTO homegroup_member (homegroup_id, member_id, join_date, is_active) VALUES(%s, %s, %s, TRUE)
        '''
        g.cursor.execute(query, (homegroup_id, member_id, date))
        g.connection.commit()
    return g.cursor.rowcount


# removes a member from a homegroup -- really just sets them inactive
def remove_member(homegroup_id, member_id):
    query = '''
    UPDATE homegroup_member SET is_active = FALSE
    WHERE homegroup_id = %s AND member_id = %s
    '''
    g.cursor.execute(query, (homegroup_id, member_id))
    g.connection.commit()
    return g.cursor.rowcount


# this sets a member as inactive in the system
def deactivate_member(member_id):
    query = '''
    UPDATE member SET is_active = FALSE
    WHERE id = %s
    '''
    g.cursor.execute(query, (member_id,))
    g.connection.commit()
    return g.cursor.rowcount


# this sets a member as active in the system
def reactivate_member(member_id):
    query = '''
    UPDATE member SET is_active = TRUE
    WHERE id = %s
    '''
    g.cursor.execute(query, (member_id,))
    g.connection.commit()
    return g.cursor.rowcount


# finds all members in a particular homegroup
def get_homegroup_members(homegroup_id):
    query = '''
        SELECT homegroup_member.member_id, first_name, last_name, email, name, homegroup_member.is_active AS "activeMember",  homegroup_leader.is_active AS "hgLeader" FROM member
        JOIN homegroup_member ON member.id = homegroup_member.member_id
        JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
        LEFT OUTER JOIN homegroup_leader ON homegroup_leader.member_id = member.id AND homegroup_leader.homegroup_id = homegroup.id
        WHERE homegroup_member.is_active = TRUE AND  homegroup.id = %s AND member.is_active = TRUE
        ORDER BY last_name, first_name
    '''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


def number_of_meetings_held(homegroup_id):
    query = ''' SELECT count(DISTINCT meeting_id) AS "numMeetings"
   FROM attendance
   WHERE homegroup_id = %s
   '''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchone()


# finds if a member has missed (number_of_misses) consecutive meetings
def system_attendance_alert(homegroup_id, member_id, number_of_misses):
    query = """
    SELECT  * FROM attendance
    WHERE homegroup_id = %s AND member_id = %s
    ORDER BY meeting_id DESC
    LIMIT %s
    """
    g.cursor.execute(query, (homegroup_id, member_id, number_of_misses))
    return g.cursor.fetchall()


def get_member_attendance(homegroup_id, member_id):
    query = '''
    SELECT  first_name, last_name, date, attendance FROM attendance
    JOIN member ON attendance.member_id = member.id
    JOIN meeting ON meeting.id = attendance.meeting_id
    WHERE homegroup_id = %s AND member_id = %s
    AND date IN (
        SELECT DISTINCT date FROM attendance
            JOIN meeting ON meeting.id = attendance.meeting_id
        WHERE homegroup_id = %s
        ORDER BY date DESC LIMIT 3
    )
    ORDER BY date DESC
    '''

    g.cursor.execute(query, (homegroup_id, member_id, homegroup_id))
    return g.cursor.fetchall()


def get_last_3_dates(homegroup_id):
    query = '''
    SELECT DISTINCT date FROM attendance
            JOIN meeting ON meeting.id = attendance.meeting_id
        WHERE homegroup_id = %s
        ORDER BY date DESC LIMIT 3'''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


# HOME GROUP ########################################


# finds a homegroup leader
def find_homegroup_leader(homegroup_id):
    homegroup_id = int(homegroup_id)
    g.cursor.execute('''
        SELECT * FROM homegroup_leader
        JOIN member ON member.id = homegroup_leader.member_id
        JOIN homegroup ON homegroup_leader.homegroup_id = homegroup.id
        WHERE homegroup_id = %s
        ''', (homegroup_id,))
    return g.cursor.fetchone()


# finds a member's homegroup
def find_member_homegroup(member_id):
    g.cursor.execute('''
       SELECT * FROM homegroup_member JOIN member ON member.id = homegroup_member.member_id
       WHERE member_id = %s
       ''', (member_id,))
    return g.cursor.fetchone()


# find if already has a homegroup
def member_already_in_homegroup(member_id):
    g.cursor.execute('''
          SELECT * FROM homegroup_member JOIN member ON member.id = homegroup_member.member_id
      
          WHERE member_id = %s AND homegroup_member.is_active = TRUE
          ''', (member_id,))
    return g.cursor.fetchone()


# finds all the attendance dates entered in a particular homegroup
def get_attendance_dates(homegroup_id):
    homegroup_id = int(homegroup_id)

    query = '''
        SELECT DISTINCT meeting.date, meeting.time, attendance.meeting_id
        FROM meeting JOIN attendance ON meeting.id = attendance.meeting_id
        WHERE homegroup_id = %s
        ORDER BY meeting.date DESC, meeting.time DESC
    '''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


# creates a new attendance report and initializes everyone's attendance to false
def generate_attendance_report(homegroup_id, meeting_id):
    members = get_homegroup_members(homegroup_id)
    for member in members:
        query = '''INSERT INTO attendance (homegroup_id, member_id, meeting_id, attendance)
        VALUES (%s, %s, %s, %s)
        '''
        g.cursor.execute(query, (homegroup_id, member['member_id'], meeting_id, False))
    g.connection.commit()
    return g.cursor.rowcount


# returns the attendance of a particular homegroup on a particular day/time
def get_attendance(homegroup_id, meeting_id):
    meeting_id = int(meeting_id)
    query = '''SELECT * FROM attendance JOIN member ON attendance.member_id = member.id
                WHERE homegroup_id = %s AND meeting_id = %s '''
    g.cursor.execute(query, (homegroup_id, meeting_id))
    return g.cursor.fetchall()


## homegroup analytics ###

def homegroup_analytics(year):
    query = '''
     SELECT  EXTRACT(MONTH FROM TO_DATE(join_date, 'MM-DD-YYYY')) AS "month", count(DISTINCT member_id)
 FROM homegroup_member
 WHERE EXTRACT(YEAR FROM TO_DATE(join_date, 'MM-DD-YYYY'))  = %s AND is_active = TRUE
 GROUP BY month
    '''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


def number_of_minors(year):
    query = '''SELECT EXTRACT(MONTH FROM TO_DATE(homegroup_member.join_date, 'MM-DD-YYYY')) AS "month", count(DISTINCT (member_id))
FROM member JOIN homegroup_member ON homegroup_member.member_id = member.id
WHERE date_part('year', age(CURRENT_DATE,to_date(birthday, 'YYYY-MM-DD'))) < 18 AND EXTRACT(YEAR FROM TO_DATE(homegroup_member.join_date, 'MM-DD-YYYY'))  = %s AND homegroup_member.is_active = TRUE
GROUP BY month'''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


def number_of_new_members(year):
    query = '''SELECT EXTRACT(MONTH FROM TO_DATE(homegroup_member.join_date, 'MM-DD-YYYY')) AS "month", count(DISTINCT (member_id))
    FROM member JOIN homegroup_member ON homegroup_member.member_id = member.id
    WHERE date_part('year', age(CURRENT_DATE,to_date(birthday, 'YYYY-MM-DD'))) >= 18 AND EXTRACT(YEAR FROM TO_DATE(homegroup_member.join_date, 'MM-DD-YYYY'))  = %s AND homegroup_member.is_active = TRUE
    GROUP BY month'''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


def members_attending_a_homegroup(year):
    query = '''SELECT EXTRACT(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')) AS "month", count (DISTINCT attendance.member_id)
FROM attendance
JOIN meeting ON meeting.id = attendance.meeting_id
WHERE attendance = TRUE AND EXTRACT(YEAR FROM TO_DATE(date, 'YYYY-MM-DD'))  = %s
GROUP BY month
'''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


def total_members(year):
    query = '''SELECT EXTRACT(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')) AS "month", count (DISTINCT attendance.member_id)
FROM attendance
JOIN meeting ON meeting.id = attendance.meeting_id
WHERE EXTRACT(YEAR FROM TO_DATE(date, 'YYYY-MM-DD'))  = %s
GROUP BY month
'''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


# finds date information from a meeting id
def find_date(meeting_id):
    g.cursor.execute('SELECT * FROM meeting WHERE id =%s', (meeting_id,))
    return g.cursor.fetchone()


# updates attendance for a homegroup's member on a particular day/time
def update_attendance(homegroup_id, member_id, meeting_id, attendance):
    query = '''
        UPDATE attendance SET attendance = %s
        WHERE homegroup_id = %s AND member_id = %s AND meeting_id = %s
        '''
    g.cursor.execute(query, (attendance, homegroup_id, member_id, meeting_id))
    g.connection.commit()
    return g.cursor.rowcount


# creates a new date or "meeting" time in the db
def add_date(date, time):
    query = '''
    INSERT INTO meeting (date, time) VALUES (%s, %s)
    '''
    g.cursor.execute(query, (date, time))
    g.connection.commit()
    query = '''SELECT id FROM meeting ORDER BY id DESC LIMIT 1'''
    g.cursor.execute(query)
    return g.cursor.fetchone()


def find_homegroup_by_id(homegroup_id):
    """Find a homegroup based on ID."""
    g.cursor.execute('SELECT * FROM homegroup WHERE id =%s', (homegroup_id,))
    return g.cursor.fetchone()


def find_homegroup_by_name(name):
    """Find a homegroup by name."""
    g.cursor.execute('SELECT * FROM homegroup WHERE name=%(name)s', {'name': name})
    return g.cursor.fetchone()


def create_homegroup(name, location, description, latitude, longitude):
    """Create a new home group"""
    now = datetime.now()
    today = now.strftime("%m-%d-%Y")
    query = '''
        INSERT INTO homegroup(name, location, description, latitude, longitude,creation_date, is_active)
        VALUES(%s, %s, %s, %s, %s, %s,  TRUE)
        RETURNING id
        '''
    g.cursor.execute(query, (name, location, description, latitude, longitude, today,))
    g.connection.commit()
    return {'id': g.cursor.fetchone()['id'], 'rowcount': g.cursor.rowcount}


def edit_homegroup(homegroup_id, name, location, description, latitude, longitude):
    """Edit a home group"""
    query = '''
    UPDATE homegroup SET name = %s, location = %s, description = %s, latitude = %s, longitude = %s
    WHERE id = %s
    '''
    g.cursor.execute(query, (name, location,
                             description, latitude, longitude, homegroup_id))
    g.connection.commit()
    return g.cursor.rowcount


# returns all homegroups
def get_all_homegroups():
    query = '''
        SELECT * FROM homegroup
        WHERE is_active=TRUE
        '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


# returns all homegroup info - including leader info etc.
def get_all_homegroup_info():
    query = '''
        SELECT * FROM homegroup LEFT OUTER JOIN homegroup_leader ON homegroup.id = homegroup_leader.homegroup_id LEFT OUTER JOIN member ON homegroup_leader.member_id = member.id
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


# returns members from the original group and the two groups into which the original group is being split
def get_split_homegroup_info(homegroup_id, homegroup1_id, homegroup2_id):
    query = '''
        SELECT homegroup_member.member_id, first_name, last_name, email, name,  homegroup_leader.is_active AS "hgLeader", homegroup.id as "group" FROM member
        JOIN homegroup_member ON member.id = homegroup_member.member_id
        JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
        LEFT OUTER JOIN homegroup_leader ON homegroup_leader.member_id = member.id AND homegroup_leader.homegroup_id = homegroup.id
        WHERE homegroup_member.is_active = TRUE AND  homegroup.id in (%s,%s,%s) AND member.is_active = true and homegroup_member.is_active = true
        ORDER BY last_name, first_name
        '''
    g.cursor.execute(query, (homegroup_id, homegroup1_id, homegroup2_id))
    return g.cursor.fetchall()

# deactivates a homegroup
def deactivate_homegroup(homegroup_id):
    query = '''
    UPDATE homegroup SET is_active = FALSE
    WHERE id = %s
    '''
    g.cursor.execute(query, (homegroup_id,))
    g.connection.commit()
    return g.cursor.rowcount


def reactivate_homegroup(homegroup_id):
    query = '''
    UPDATE homegroup SET is_active = TRUE
    WHERE id = %s
    '''
    g.cursor.execute(query, (homegroup_id,))
    g.connection.commit()
    return g.cursor.rowcount


def number_of_members_in_homegroup(homegroup_id):
    query = '''
    SELECT count(DISTINCT member_id) AS "numMembers" FROM homegroup_member 
    JOIN member ON member.id = homegroup_member.member_id
    WHERE homegroup_member.is_active = TRUE AND member.is_active = TRUE
    AND homegroup_id = %s'''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchone()


def get_all_inactive_homegroups():
    query = '''
    SELECT * FROM homegroup
    WHERE is_active=FALSE
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def get_homegroup_attendance_records(homegroup_id):
    query = ''' SELECT date, time,  first_name, last_name, attendance FROM attendance
    JOIN member ON member.id = attendance.member_id
    JOIN meeting ON meeting.id = attendance.meeting_id 
    WHERE homegroup_id = %s'''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


def get_all_homegroup_attendance_records():
    query = ''' SELECT name AS "Home Group", date, time,  first_name, last_name, attendance FROM attendance
        JOIN member ON member.id = attendance.member_id
        JOIN meeting ON meeting.id = attendance.meeting_id 
        JOIN homegroup ON attendance.homegroup_id = homegroup.id
        '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


#################################### Admin ########################################

# finds all active admin in the db
def get_all_admin():
    query = '''
        SELECT * FROM member
        JOIN member_role ON member.id = member_role.member_id
        JOIN role ON member_role.role_id = role.id
        WHERE role.role="admin" AND member_role.is_active = TRUE AND member.is_active = TRUE
        '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


# finds all inactive admin in the db
def get_all_inactive_admin():
    query = '''
    SELECT * FROM member
     JOIN member_role ON member.id = member_role.member_id
        JOIN role ON member_role.role_id = role.id
    WHERE role.role="admin" AND member_role.is_active = FALSE AND member.is_active = FALSE
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def get_attendance_counts():
    query = '''
SELECT  to_char(to_timestamp(to_char(extract(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')), '999'), 'MM'), 'Mon') AS "month", COUNT (DISTINCT member.id) AS "countMembers" FROM attendance
    JOIN meeting ON attendance.meeting_id = meeting.id
    JOIN member ON attendance.member_id = member.id
    JOIN homegroup ON  homegroup.id = attendance.homegroup_id
    WHERE attendance = TRUE
    GROUP BY month
    ORDER BY month ASC
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def get_top_n_homegroup_member_counts(n):
    n = int(n)
    query = '''
    SELECT name, count(DISTINCT member_id) AS memberCount FROM homegroup_member
    JOIN member ON member.id = homegroup_member.member_id
    JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
    WHERE homegroup_member.is_active = TRUE AND member.is_active = TRUE
    AND homegroup.is_active = TRUE
    GROUP BY name
    ORDER BY memberCount DESC LIMIT %s
    '''
    g.cursor.execute(query, (n,))
    return g.cursor.fetchall()


def gender_report():
    query = '''
     SELECT gender, count(DISTINCT member_id) AS memberCount FROM homegroup_member
    JOIN member ON member.id = homegroup_member.member_id
    JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
    WHERE homegroup_member.is_active = TRUE AND member.is_active = TRUE
    GROUP BY gender
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def homegroup_member_attendance(homegroup_id):
    query = '''
       SELECT first_name, last_name, date, attendance
   FROM attendance JOIN meeting ON meeting.id = attendance.meeting_id
   JOIN member ON attendance.member_id = member.id
   WHERE homegroup_id = %s AND date IN (
       SELECT DISTINCT date FROM attendance
       JOIN meeting ON meeting_id = meeting.id
       WHERE homegroup_id = %s
       ORDER BY date DESC LIMIT 3
   )
   ORDER BY first_name, last_name, date DESC
    '''
    g.cursor.execute(query, (homegroup_id, homegroup_id))
    return g.cursor.fetchall()


def get_homegroup_attendance_counts(myhomegroup):
    query = '''
    SELECT to_char(to_timestamp(to_char(extract(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')), '999'), 'MM'), 'Mon') AS "month", extract(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')) AS "month_num", COUNT( DISTINCT member.id) AS "countMembers" FROM attendance
    JOIN meeting ON attendance.meeting_id = meeting.id
    JOIN member ON attendance.member_id = member.id
    WHERE attendance = TRUE AND homegroup_id = %s
    GROUP BY month, month_num
    ORDER BY month_num ASC

    '''
    g.cursor.execute(query, (myhomegroup,))
    return g.cursor.fetchall()


def get_all_members_emails():
    query = '''
    SELECT email
    FROM member
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def get_homegroup_emails(homegroup_id):
    query = '''
    SELECT email FROM member
        JOIN homegroup_member ON member.id = homegroup_member.member_id
        JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
    WHERE homegroup_id = %s'''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


################## Analytics #############################################

# total number of home groups created
def number_of_homegroups():
    query = ''' SELECT count(id) AS "numberOfHomegroups" FROM homegroup
        '''
    g.cursor.execute(query)
    return g.cursor.fetchone()


# total number of active home groups
def number_of_active_homegroups():
    query = '''
            SELECT count(id) AS "numberOfHomegroups" FROM homegroup
            WHERE is_active = TRUE
            '''
    g.cursor.execute(query)
    return g.cursor.fetchone()


# total number of members attending home groups
def number_of_members_attending_homegroups():
    query = '''
            SELECT count(DISTINCT (homegroup_member.member_id)) AS "numberOfMembers" FROM homegroup_member
            JOIN attendance ON homegroup_member.member_id = attendance.member_id
            WHERE homegroup_member.is_active = TRUE
            '''
    g.cursor.execute(query)
    return g.cursor.fetchone()


# attendance rate for the current month
def attendance_rate_for_current_month(month):
    total_attended = 0
    total_people = 0
    homegroups = get_all_homegroups()
    for hg in homegroups:
        total_attended = total_attended + people_who_attended(month, hg['id'])['members']
        total_people = total_people + total_in_homegroup(month, hg['id'])['totalMembers']
    if (total_attended == 0) or (total_people == 0):
        percentage = 0
    else:
        percentage = (total_attended / total_people) * 100
    return percentage


# attendance rate for the current month for a homegroup
def get_homegroup_attendance_rate(month, homegroup_id):
    total_attended = people_who_attended(month, homegroup_id)['members']
    total_people = total_in_homegroup(month, homegroup_id)['totalMembers']

    if (total_attended == 0) or (total_people == 0):
        percentage = 0
    else:
        percentage = (total_attended / total_people) * 100
    return percentage


def people_who_attended(month, homegroup_id):
    query = '''SELECT count(( member_id ))AS "members"
        FROM attendance JOIN meeting ON meeting.id = attendance.meeting_id
WHERE attendance = TRUE AND extract(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')) = %s
AND homegroup_id = %s
                '''
    g.cursor.execute(query, (month, homegroup_id))
    return g.cursor.fetchone()


def total_in_homegroup(month, homegroup_id):
    query = '''SELECT count( (member_id ))AS "totalMembers"
        FROM attendance JOIN meeting ON meeting.id = attendance.meeting_id
WHERE extract(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')) = %s AND homegroup_id = %s
                '''
    g.cursor.execute(query, (month, homegroup_id))
    return g.cursor.fetchone()


# number of home group leaders
def number_of_homegroup_leaders():
    query = '''
            SELECT count(DISTINCT(member_id)) AS "numberOfHomegroupLeaders" FROM homegroup_leader
            WHERE is_active = TRUE
            '''
    g.cursor.execute(query)
    return g.cursor.fetchone()
