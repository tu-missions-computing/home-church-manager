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
    query = '''
    INSERT INTO member_role(member_id, password, role_id, is_active)
    VALUES(%s, %s, %s, %s);
    '''
    g.cursor.execute(query, (member_id, password, role_id, True))
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


def find_roles():
    query = '''
    SELECT * FROM role
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


# finds all the members and their roles
def get_all_member_roles():
    query = '''
    select first_name, last_name, member.id, homegroup_id, role_id, role, member_role.is_active as "roleActive", homegroup_leader.is_active as "hgLeaderActive", name as "hgName" from member 
    left outer join member_role on member.id = member_role.member_id 
    left outer join homegroup_leader on member.id = homegroup_leader.member_id
    left outer join role on member_role.role_id = role.id 
    left outer join homegroup on homegroup_leader.homegroup_id = homegroup.id
    where member.is_active = TRUE
    order by last_name, first_name
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
    g.cursor.execute('SELECT * from member join member_role on member_role.member_id = member.id WHERE member.id =%s',
                     (id,))
    return g.cursor.fetchone()


# finds if the user is active
def is_role_active(id, role_id):
    g.cursor.execute('select is_active from member_role where member_id = %s and role_id = %s', (id, role_id))
    return g.cursor.fetchone()


# finds if the user has an active role
def has_active_role(id):
    g.cursor.execute('''select is_active from member_role where member_id = %s and is_active = TRUE ''', (id,))
    return g.cursor.fetchone()


# updates the user role
def update_role(id, role_id, is_active):
    query = '''
        UPDATE member_role SET is_active = %s
        where member_id = %s and role_id = %s
        '''
    g.cursor.execute(query, (is_active, id, role_id))
    g.connection.commit()
    return g.cursor.rowcount


# retrieves all the marital status
def get_marital_status():
    query = ''' select * from marital_status '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def get_marital_status_by_name(name):
    g.cursor.execute('SELECT * FROM marital_status WHERE marital_status_name=%(name)s', {'name': name})
    return g.cursor.fetchone()


# retrieves all the methods of finding out about the homegroups/church
def get_how_did_you_find_out():
    g.cursor.execute('SELECT * FROM how_did_you_find_out ')
    return g.cursor.fetchall()


def get_how_did_you_find_out_by_name(name):
    g.cursor.execute('SELECT * FROM how_did_you_find_out WHERE how_did_you_find_out_name=%(name)s', {'name': name})
    return g.cursor.fetchone()


# updates the user role from admin role view based on selection
def assign_new_role(id, role_id):
    query = '''
    update member_role set is_active = TRUE, role_id = %s where member_id = %s
    '''
    g.cursor.execute(query, (role_id, id))
    g.connection.commit()
    return g.cursor.rowcount


# finds the most recent member entered into the db
def recent_user():
    g.cursor.execute('select id from member order by id desc LIMIT 1')
    return g.cursor.fetchone()


# grabs all members in the db
def get_all_users():
    query = '''
        SELECT * FROM member_role
      JOIN role on member_role.role_id = role.id
      JOIN member on member.id = member_role.member_id
        '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


# finds a members associated homegroup (specifically for homegroup leaders)
def find_user_homegroup(email):
    g.cursor.execute(
        'SELECT * from homegroup_leader JOIN member on homegroup_leader.member_id = member.id WHERE email = %s',
        (email,))
    return g.cursor.fetchone()['homegroup_id']


# finds the most recent member entered into the db
def recent_user():
    g.cursor.execute('select id from member order by id desc LIMIT 1')
    return g.cursor.fetchone()


#################################### MEMBER ########################################

# returns a count of all members in the db
def get_member_count():
    query = '''
        SELECT count(id)
        FROM member
        '''
    return g.cursor.execute(query).fetchall()


# finds member info by passing in an email
def find_member_info(email):
    g.cursor.execute('SELECT * from member WHERE email =%s', (email,))
    return g.cursor.fetchone()


# finds member info by passing in a member id
def find_member(member_id):
    g.cursor.execute('SELECT * FROM member WHERE id = %s', (member_id,))
    return g.cursor.fetchone()


# finds all members in the db
def get_all_members():
    query = '''
    SELECT * FROM member
    WHERE is_active=TRUE
    ORDER BY last_name asc
    '''
    g.cursor.execute(query)
    return add_age_to_member_rows(g.cursor.fetchall())


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
    query = '''
    select * from member where member.is_active = TRUE and member.id not in (
    select member_id from homegroup_member
    where homegroup_id = %s and
    homegroup_member.is_active = TRUE
    )
    '''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


# finds all the inactive homegroup members
def get_homegroup_inactive_members(homegroup_id):
    g.cursor.execute('''SELECT * FROM member
            JOIN homegroup_member ON member.id = homegroup_member.member_id
            JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
            WHERE homegroup_member.is_active != TRUE and  homegroup.id = %s
            order by last_name, first_name''', (homegroup_id,))
    return g.cursor.fetchall()


# sets a homegroup member to be reactivated in the homegroup
def reactive_homegroup_member(homegroup_id, member_id):
    query = '''
    UPDATE homegroup_member SET is_active = TRUE
    where homegroup_id = %s and member_id = %s
    '''
    g.cursor.execute(query, (homegroup_id, member_id))
    g.connection.commit()
    return g.cursor.rowcount


# finds all inactive members in the db
def get_all_inactive_members():
    query = '''
    SELECT * FROM member
    WHERE is_active=FALSE
    order by last_name, first_name
    '''
    g.cursor.execute(query)
    return add_age_to_member_rows(g.cursor.fetchall())


# edits member info
def edit_member(member_id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status,
                how_did_you_find_out, is_a_parent, join_date):
    member_id = int(member_id)

    query = '''
    UPDATE member SET first_name = %s, last_name = %s, email = %s, phone_number = %s, gender = %s, birthday = %s, baptism_status = %s, marital_status_id = %s, how_did_you_find_out_id = %s, is_a_parent = %s,  join_date = %s
    WHERE id = %s
    '''
    g.cursor.execute(query, (
        first_name, last_name, email, phone_number, gender, birthday, baptism_status, marital_status,
        how_did_you_find_out,
        is_a_parent, join_date, member_id))
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
    return { 'id': g.cursor.fetchone()['id'], 'rowcount': g.cursor.rowcount }


# adds leader to a homegroup
def add_leader_to_homegroup(member_id, homegroup_id):
    g.cursor.execute('select * from homegroup_leader where member_id =%s ', (member_id,))
    if (g.cursor.fetchone()):
        query = '''update homegroup_leader set is_active = TRUE, homegroup_id = %s where member_id = %s'''
        g.cursor.execute(query, (homegroup_id, member_id))
    else:
        query = '''
        INSERT INTO homegroup_leader(member_id, homegroup_id, is_active) values(%s, %s, TRUE)
        '''
        g.cursor.execute(query, (member_id, homegroup_id))
    g.connection.commit()
    return g.cursor.rowcount


# deactivates hg leader

def deactivate_hgleader(member_id, homegroup_id):
    query = '''
    update  homegroup_leader set is_active = FALSE
    where member_id = %s and homegroup_id = %s
    '''
    g.cursor.execute(query, (member_id, homegroup_id))
    g.connection.commit()
    deactivate_hgleader_role(member_id)
    return g.cursor.rowcount


def deactivate_hgleader_role(member_id):
    query = '''
        update member_role set is_active = False
        where member_id = %s '''
    g.cursor.execute(query, (member_id,))
    g.connection.commit()
    return g.cursor.rowcount


# adds a member to a homegroup
def add_member_to_homegroup(homegroup_id, member_id):
    now = datetime.now()
    date = now.strftime("%m-%d-%Y")
    query = '''
    INSERT INTO homegroup_member (homegroup_id, member_id, join_date, is_active) values(%s, %s, %s, TRUE)
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
        SELECT homegroup_member.member_id, first_name, last_name, email, name, homegroup_member.is_active as "activeMember",  homegroup_leader.is_active as "hgLeader" FROM member
        JOIN homegroup_member ON member.id = homegroup_member.member_id
        JOIN homegroup ON homegroup_member.homegroup_id = homegroup.id
        left outer join homegroup_leader on homegroup_leader.member_id = member.id and homegroup_leader.homegroup_id = homegroup.id
        WHERE homegroup_member.is_active = TRUE and  homegroup.id = %s and member.is_active = TRUE
        order by last_name, first_name
    '''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


def number_of_meetings_held(homegroup_id):
    query = ''' select count(distinct meeting_id) as "numMeetings"
   from attendance
   where homegroup_id = %s
   '''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchone()


# finds if a member has missed (number_of_misses) consecutive meetings
def system_attendance_alert(homegroup_id, member_id, number_of_misses):
    query = """
    SELECT  * FROM attendance
    WHERE homegroup_id = %s and member_id = %s
    ORDER BY meeting_id desc
    LIMIT %s
    """
    g.cursor.execute(query, (homegroup_id, member_id, number_of_misses))
    return g.cursor.fetchall()


def get_member_attendance(homegroup_id, member_id):
    query = '''
    SELECT  first_name, last_name, date, attendance FROM attendance
    join member on attendance.member_id = member.id
    join meeting on meeting.id = attendance.meeting_id
    WHERE homegroup_id = %s and member_id = %s
    and date in (
        select distinct date from attendance
            join meeting on meeting.id = attendance.meeting_id
        where homegroup_id = %s
        order by date desc limit 3
    )
    order by date desc
    '''

    g.cursor.execute(query, (homegroup_id, member_id, homegroup_id))
    return g.cursor.fetchall()


def get_last_3_dates(homegroup_id):
    query = '''
    select distinct date from attendance
            join meeting on meeting.id = attendance.meeting_id
        where homegroup_id = %s
        order by date desc limit 3'''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


#################################### HOME GROUP ########################################


# finds a homegroup leader
def find_homegroup_leader(homegroup_id):
    homegroup_id = int(homegroup_id)
    g.cursor.execute('''
        SELECT * from homegroup_leader
        join member on member.id = homegroup_leader.member_id
        join homegroup on homegroup_leader.homegroup_id = homegroup.id
        where homegroup_id = %s
        ''', (homegroup_id,))
    return g.cursor.fetchone()


# finds a member's homegroup
def find_member_homegroup(member_id):
    g.cursor.execute('''
       SELECT * from homegroup_member join member on member.id = homegroup_member.member_id
       where member_id = %s
       ''', (member_id,))
    return g.cursor.fetchone()


# find if already has a homegroup
def member_already_in_homegroup(member_id):
    g.cursor.execute('''
          SELECT * from homegroup_member join member on member.id = homegroup_member.member_id
      
          where member_id = %s and homegroup_member.is_active = TRUE
          ''', (member_id,))
    return g.cursor.fetchone()


# finds all the attendance dates entered in a particular homegroup
def get_attendance_dates(homegroup_id):
    homegroup_id = int(homegroup_id)

    query = '''
        SELECT DISTINCT meeting.date, meeting.time, attendance.meeting_id
        from meeting JOIN attendance on meeting.id = attendance.meeting_id
        WHERE homegroup_id = %s
        order by meeting.date desc, meeting.time desc
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
    query = '''SELECT * from attendance join member on attendance.member_id = member.id
                WHERE homegroup_id = %s and meeting_id = %s '''
    g.cursor.execute(query, (homegroup_id, meeting_id))
    return g.cursor.fetchall()


## homegroup analytics ###

def homegroup_analytics(year):
    query = '''
     select  EXTRACT(MONTH FROM TO_DATE(join_date, 'MM-DD-YYYY')) as "month", count(distinct member_id)
 from homegroup_member
 where EXTRACT(year FROM TO_DATE(join_date, 'MM-DD-YYYY'))  = %s and is_active = TRUE
 group by month
    '''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


def number_of_minors(year):
    query = '''select EXTRACT(MONTH FROM TO_DATE(homegroup_member.join_date, 'MM-DD-YYYY')) as "month", count(distinct (member_id))
FROM member JOIN homegroup_member on homegroup_member.member_id = member.id
WHERE date_part('year', age(CURRENT_DATE,to_date(birthday, 'YYYY-MM-DD'))) < 18 and EXTRACT(year FROM TO_DATE(homegroup_member.join_date, 'MM-DD-YYYY'))  = %s and homegroup_member.is_active = TRUE
group by month'''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


def number_of_new_members(year):
    query = '''select EXTRACT(MONTH FROM TO_DATE(homegroup_member.join_date, 'MM-DD-YYYY')) as "month", count(distinct (member_id))
    FROM member JOIN homegroup_member on homegroup_member.member_id = member.id
    WHERE date_part('year', age(CURRENT_DATE,to_date(birthday, 'YYYY-MM-DD'))) >= 18 and EXTRACT(year FROM TO_DATE(homegroup_member.join_date, 'MM-DD-YYYY'))  = %s and homegroup_member.is_active = TRUE
    group by month'''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


def members_attending_a_homegroup(year):
    query = '''select EXTRACT(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')) as "month", count (distinct attendance.member_id)
from attendance
join meeting on meeting.id = attendance.meeting_id
where attendance = true and EXTRACT(year FROM TO_DATE(date, 'YYYY-MM-DD'))  = %s
group by month
'''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


def total_members(year):
    query = '''select EXTRACT(MONTH FROM TO_DATE(date, 'YYYY-MM-DD')) as "month", count (distinct attendance.member_id)
from attendance
join meeting on meeting.id = attendance.meeting_id
where EXTRACT(year FROM TO_DATE(date, 'YYYY-MM-DD'))  = %s
group by month
'''
    g.cursor.execute(query, (year,))
    return g.cursor.fetchall()


# finds date information from a meeting id
def find_date(meeting_id):
    g.cursor.execute('SELECT * from meeting WHERE id =%s', (meeting_id,))
    return g.cursor.fetchone()


# updates attendance for a homegroup's member on a particular day/time
def update_attendance(homegroup_id, member_id, meeting_id, attendance):
    query = '''
        UPDATE attendance SET attendance = %s
        WHERE homegroup_id = %s and member_id = %s and meeting_id = %s
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
    query = '''SELECT id from meeting order by id desc limit 1'''
    g.cursor.execute(query)
    return g.cursor.fetchone()


# returns the most recent homegroup added to the db
def recent_homegroup():
    g.cursor.execute('select id from homegroup order by id desc LIMIT 1')
    return g.cursor.fetchone()


def find_homegroup_by_id(homegroup_id):
    """Find a homegroup based on ID."""
    g.cursor.execute('SELECT * from homegroup WHERE id =%s', (homegroup_id,))
    return g.cursor.fetchone()


def find_homegroup_by_name(name):
    """Find a homegroup by name."""
    g.cursor.execute('SELECT * FROM homegroup WHERE name=%(name)s', {'name': name})
    return g.cursor.fetchone()


# creates a new homegroup
def create_homegroup(name, location, description, latitude, longitude):
    now = datetime.now()
    date = now.strftime("%m-%d-%Y")
    query = '''
        INSERT INTO homegroup(name, location, description, latitude, longitude,creation_date, is_active)
        VALUES(%s, %s, %s, %s, %s, %s,  TRUE)
        '''
    g.cursor.execute(query, (name, location, description, latitude, longitude, date,))
    g.connection.commit()
    return g.cursor.rowcount


# edits homegroup info
def edit_homegroup(homegroup_id, name, location, description, latitude, longitude):
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
        select * from homegroup left outer join homegroup_leader on homegroup.id = homegroup_leader.homegroup_id left outer join member on homegroup_leader.member_id = member.id
    '''
    g.cursor.execute(query)
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
    select count(distinct member_id) as "numMembers" from homegroup_member 
    join member on member.id = homegroup_member.member_id
    where homegroup_member.is_active = TRUE and member.is_active = TRUE
    and homegroup_id = %s'''
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
    query = ''' select date, time,  first_name, last_name, attendance from attendance
    join member on member.id = attendance.member_id
    join meeting on meeting.id = attendance.meeting_id 
    WHERE homegroup_id = %s'''
    g.cursor.execute(query, (homegroup_id,))
    return g.cursor.fetchall()


def get_all_homegroup_attendance_records():
    query = ''' select name As "Home Group", date, time,  first_name, last_name, attendance from attendance
        join member on member.id = attendance.member_id
        join meeting on meeting.id = attendance.meeting_id 
        join homegroup on attendance.homegroup_id = homegroup.id
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
SELECT  to_char(to_timestamp(to_char(extract(month from TO_DATE(date, 'YYYY-MM-DD')), '999'), 'MM'), 'Mon') as "month", COUNT (DISTINCT member.id) AS "countMembers" FROM attendance
    JOIN meeting ON attendance.meeting_id = meeting.id
    JOIN member ON attendance.member_id = member.id
    JOIN homegroup on  homegroup.id = attendance.homegroup_id
    WHERE attendance = TRUE
    GROUP BY month
    order by month asc
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def get_top_n_homegroup_member_counts(n):
    n = int(n)
    query = '''
    select name, count(distinct member_id) as memberCount from homegroup_member
    join member on member.id = homegroup_member.member_id
    join homegroup on homegroup_member.homegroup_id = homegroup.id
    where homegroup_member.is_active = TRUE and member.is_active = TRUE
    and homegroup.is_active = TRUE
    group by name
    order by memberCount desc limit %s
    '''
    g.cursor.execute(query, (n,))
    return g.cursor.fetchall()


def gender_report():
    query = '''
     select gender, count(distinct member_id) as memberCount from homegroup_member
    join member on member.id = homegroup_member.member_id
    join homegroup on homegroup_member.homegroup_id = homegroup.id
    where homegroup_member.is_active = TRUE and member.is_active = TRUE
    group by gender
    '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def homegroup_member_attendance(homegroup_id):
    query = '''
       select first_name, last_name, date, attendance
   from attendance join meeting on meeting.id = attendance.meeting_id
   join member on attendance.member_id = member.id
   where homegroup_id = %s and date in (
       select distinct date from attendance
       join meeting on meeting_id = meeting.id
       where homegroup_id = %s
       order by date desc limit 3
   )
   order by first_name, last_name, date desc
    '''
    g.cursor.execute(query, (homegroup_id, homegroup_id))
    return g.cursor.fetchall()


def get_homegroup_attendance_counts(myhomegroup):
    query = '''
    SELECT to_char(to_timestamp(to_char(extract(month from TO_DATE(date, 'YYYY-MM-DD')), '999'), 'MM'), 'Mon') as "month", extract(month from TO_DATE(date, 'YYYY-MM-DD')) as "month_num", COUNT( distinct member.id) AS "countMembers" FROM attendance
    JOIN meeting ON attendance.meeting_id = meeting.id
    JOIN member ON attendance.member_id = member.id
    WHERE attendance = TRUE AND homegroup_id = %s
    GROUP BY month, month_num
    order by month_num asc

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
    query = ''' select count(id) as "numberOfHomegroups" from homegroup
        '''
    g.cursor.execute(query)
    return g.cursor.fetchone()


# total number of active home groups
def number_of_active_homegroups():
    query = '''
            select count(id) as "numberOfHomegroups" from homegroup
            where is_active = TRUE
            '''
    g.cursor.execute(query)
    return g.cursor.fetchone()


# total number of members attending home groups
def number_of_members_attending_homegroups():
    query = '''
            select count(distinct (homegroup_member.member_id)) as "numberOfMembers" from homegroup_member
            join attendance on homegroup_member.member_id = attendance.member_id
            where homegroup_member.is_active = TRUE
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
    query = '''select count(( member_id ))as "members"
        from attendance join meeting on meeting.id = attendance.meeting_id
where attendance = TRUE and extract(month from TO_DATE(date, 'YYYY-MM-DD')) = %s
and homegroup_id = %s
                '''
    g.cursor.execute(query, (month, homegroup_id))
    return g.cursor.fetchone()


def total_in_homegroup(month, homegroup_id):
    query = '''select count( (member_id ))as "totalMembers"
        from attendance join meeting on meeting.id = attendance.meeting_id
where extract(month from TO_DATE(date, 'YYYY-MM-DD')) = %s and homegroup_id = %s
                '''
    g.cursor.execute(query, (month, homegroup_id))
    return g.cursor.fetchone()


# number of home group leaders
def number_of_homegroup_leaders():
    query = '''
            select count(distinct(member_id)) as "numberOfHomegroupLeaders" from homegroup_leader
            where is_active = TRUE
            '''
    g.cursor.execute(query)
    return g.cursor.fetchone()
