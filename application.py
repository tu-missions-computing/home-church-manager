from functools import wraps

from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, RadioField, SubmitField, IntegerField, DateField
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Email, Length, DataRequired, NumberRange, InputRequired, EqualTo
from wtforms.validators import Length
from wtforms import validators
from flask_bcrypt import Bcrypt

import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'

bcrypt = Bcrypt(app)
login_mgr = LoginManager()
login_mgr = LoginManager(app)


@app.before_request
def before():
    db.open_db_connection()


@app.teardown_request
def after(exception):
    db.close_db_connection()




#this initializes some test users -- we can no longer do this in the db because of the password hashing
def init_test_user():
    if db.find_user('john@example.com') is None:
        password = 'password'
        pw_hash = bcrypt.generate_password_hash(password)
        db.create_user('john@example.com', pw_hash, 2)
    if db.find_user('admin@example.com') is None:
        password = 'password'
        pw_hash = bcrypt.generate_password_hash(password)
        db.create_user('admin@example.com', pw_hash, 3)


########################## INDEX + MAP + Dashboard##############################################

#this takes the user to the index page which is a map of all the homegroups
@app.route('/')
def index():
# return redirect(url_for("homegroup", homegroup_id=session['homegroup_id']))
   return render_template('index.html')

#this displays the dashboard depending on user role
@app.route('/dashboard')
def dashboard():
    email = current_user.email
    role = current_user.role
    if role == 'homegroup_leader':
        homegroup_id = db.find_user_homegroup(email)
        return redirect(url_for('homegroup', homegroup_id = homegroup_id))
    if role =="admin":
        return redirect(url_for('admin_home'))

#displays the map of all the homegroups
@app.route('/map')
def map():
    homegroups = db.get_all_homegroups()
    return render_template('map.html', homegroups = homegroups)


########################## USER + LOGIN ##############################################

#this allows/disallows users from accessing pages based on their roles
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not hasattr(current_user, 'role'):
                flash('User does not have sufficient privileges ')
                return redirect(url_for('index'))
            elif current_user.role not in roles:
                flash( 'User does not have sufficient privileges ')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

class UserForm(FlaskForm):
    email = StringField('E-mail Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Change Role', choices=[], coerce=int)
    homegroups = SelectField('Choose Homegroup', choices=[], coerce=int)
    submit = SubmitField('Create User')

#Creates a new user and hashes their password in the database
@app.route('/user/create/<member_id>', methods=['GET', 'POST'])
def create_user(member_id):
    allRoles = db.find_roles()
    roleList = []
    for role in allRoles:
        roleList.append((role["id"], role["role"]))
    member = db.find_member(member_id)
    email = member['email']
    user_form = UserForm( email = member['email'])
    user_form.role.choices = roleList

    homegroups = db.get_all_homegroups()
    homegroup_list = []
    for homegroup in homegroups:
        homegroup_list.append((homegroup['id'], homegroup['name']))
    user_form.homegroups.choices = homegroup_list

    if user_form.validate_on_submit():
        password = user_form.password.data
        pw_hash = bcrypt.generate_password_hash(password)
        db.create_user(user_form.email.data, pw_hash, user_form.role.data)
        if user_form.homegroups.data is not None:
            homegroupId = user_form.homegroups.data
            user_id =  db.find_user(email)['id']
            db.add_leader_to_homegroup(user_id, homegroupId)



        flash('User Created')
        return redirect(url_for('all_members'))
    return render_template('create_user.html', form=user_form)

class User(object):
    """Class for the currently logged-in user (if there is one). Only stores the user's e-mail."""
    def __init__(self, email):
        self.email = email
        if db.find_user(self.email) is not None:
            self.role = db.find_user(self.email)['role']
            self.name = db.find_member_info(self.email)['first_name']
        else:
            self.role = 'no role'
            self.name = 'no name'
        if (self.role == 'homegroup_leader'):
            self.homegroup_id = db.find_user_homegroup(self.email)

        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        """Return the unique ID for this user. Used by Flask-Login to keep track of the user in the session object."""
        return self.email

    def get_role(self):
        """Returns the role of the user from the db"""
        return self.role

    def __repr__(self):
        return "<User '{}' {} {} {} {}>".format(self.email, self.role,  self.is_authenticated, self.is_active, self.is_anonymous)


@login_mgr.user_loader
def load_user(id):
    """Return the currently logged-in user when given the user's unique ID"""
    return User(id)

#checks to see if the password entered matches the hash password
def authenticate(email, password):
    """Check whether the arguments match a user from the "database" of valid users."""
    valid_users = db.get_all_users()
    for user in valid_users:
        if email == user['email'] and bcrypt.check_password_hash(user['password'], password):
            return email
    return None

class LoginForm(FlaskForm):
    email = StringField('E-mail Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

#logs the user in, creates a new session, and creates a current user which is of the class "User"
@app.route('/login', methods=['GET', 'POST'])
def login():
    #temporary
    init_test_user()
    login_form = LoginForm()
    print (request.form)
    if login_form.validate_on_submit():
        if authenticate(login_form.email.data, login_form.password.data):
            # Credentials authenticated.
            # Create the user object, let Flask-Login know, and redirect to the home page
            current_user = User(login_form.email.data)
            login_user(current_user)
            session['username'] = current_user.email
            flash('Logged in successfully as {}'.format(login_form.email.data))
            return redirect(url_for('dashboard'))
        else:
            # Authentication failed.
            flash('Invalid email address or password')
            return redirect(url_for('index'))

    return render_template('login.html', form = login_form)


#logs the user out and removes the session
@app.route('/logout')
def logout():
    logout_user()
    user_name = session.pop('username', None)
    flash('Logged out')
    return redirect(url_for('index'))





########################## HOME GROUP  (Home Group Leader)##############################################

#this is the homegroup main page / dashboard
@app.route('/homegroup/<homegroup_id>')
@login_required
@requires_roles('homegroup_leader', 'admin')
def homegroup(homegroup_id):
    homegroup = db.find_homegroup(homegroup_id)
    attendance_count = db.get_homegroup_attendance_counts(homegroup_id)
    return render_template('homegroup.html', currentHomegroup=homegroup,
                           attendance_count=attendance_count)

class AttendanceForm(FlaskForm):
    # member_id = StringField('member Id', validators=[Length(min=1, max=40)])
    # meeting_id = StringField('Meeting Id', validators=[Length(min=1, max=40)])
    radio = RadioField('Attendance', choices=["y","n"])
    submit = SubmitField('Submit')



#this is the default attendance page (allows you to select date/time then generate an attendance report)
@app.route('/homegroup/attendance/<homegroup_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('homegroup_leader')
def attendance(homegroup_id):
    error = ""
    attendance_form = AttendanceForm()
    members = db.get_homegroup_members(homegroup_id)
    show_members = 'N'
    if (request.method == "POST"):
        date = request.form['AttendanceDate']
        time = request.form['AttendanceTime']
        meeting_id = db.add_date(date, time)['id']
        db.generate_attendance_report(homegroup_id, meeting_id)
        return redirect(url_for('edit_attendance', homegroup_id = homegroup_id,  meeting_id = meeting_id))
    return render_template('attendance.html', currentHomegroup = homegroup_id, form=attendance_form, members=members, showmembers = show_members)

#adds (or updates) a new entry of attendance into the db
@app.route('/homegroup/attendance/add/<homegroup_id>/<member_id>/<meeting_id>/<attendance>')
@login_required
@requires_roles('homegroup_leader')
def updateAttendance(homegroup_id, member_id, attendance, meeting_id ):
    db.update_attendance(homegroup_id, member_id, meeting_id, attendance)
    return redirect(url_for('edit_attendance', homegroup_id=homegroup_id, meeting_id=meeting_id))

#This allows you to edit homegroup attendance
@app.route('/homegroup/attendance/edit/<homegroup_id>/<meeting_id>')
@login_required
@requires_roles('homegroup_leader')
def edit_attendance(homegroup_id, meeting_id):
    members = db.get_attendance(homegroup_id, meeting_id)
    date = db.find_date(meeting_id)['date']
    time = db.find_date(meeting_id)['time']
    return render_template('edit_attendance.html', currentHomegroup = homegroup_id, meeting_id = meeting_id, members = members, date = date, time = time)



#returns all the attendance dates -- this is for the attendance reports page
@app.route('/homegroup/attendance/dates/<homegroup_id>', methods=['GET'])
@login_required
@requires_roles('homegroup_leader', 'admin')
def get_attendance_dates(homegroup_id):
    return render_template('attendance_reports.html', currentHomegroup=homegroup_id, records=db.get_attendance_dates(homegroup_id))


#edit a particular homegroup
@app.route('/homegroup/edit/<homegroup_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('homegroup_leader', 'admin')
def edit_homegroup(homegroup_id):
    row = db.find_homegroup(homegroup_id)
    hg_form = CreateHomeGroupForm( name = row['name'],
                                description = row['description'],
                                location = row['location'],
                                latitude = row['latitude'],
                                longitude = row['longitude'])
    if hg_form.validate_on_submit():
        rowcount = db.edit_homegroup(homegroup_id, hg_form.name.data, hg_form.location.data, hg_form.description.data, hg_form.latitude.data, hg_form.longitude.data)
        if (rowcount == 1):
            flash("Home Group updated!")
            if (current_user.role == 'admin'):
                return redirect(url_for('get_homegroups'))
            return redirect(url_for('homegroup', homegroup_id = homegroup_id))

    return render_template('edit_homegroup.html', form = hg_form)


#this is the iframe that is in the creating/editing homegroup -- allows you to type in address and finds location
@app.route('/homegroup/select_location')
def select_location():
    return render_template('select_location.html')


########################## MEMBER (Home Group Leader) ##############################################


class CreateMemberForm(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=2, max=30, message="First name is a required field")])
    last_name = StringField('Last Name', [validators.Length(min=2, max=30, message="Last name is a required field")])
    email = StringField('Email', [validators.Email("Please enter valid email")])
    phone_number = IntegerField('Phone Number', [validators.InputRequired(message="Please enter valid phone number")])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    baptism_status = SelectField('Baptized?', choices=[('1', 'Yes'), ('0', 'No')])
    submit = SubmitField('Save Member')

#creates a new member for a particular homegroup
@app.route('/homegroup/create_member/<homegroup_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('homegroup_leader', 'admin')
def create_new_member_for_homegroup(homegroup_id):
    member = CreateMemberForm()
    if request.method == "POST" and member.validate():
        first_name = member.first_name.data
        last_name = member.last_name.data
        email = member.email.data
        phone_number = member.phone_number.data
        gender = member.gender.data
        birthday = request.form['Birthday']
        baptism_status = member.baptism_status.data
        join_date = request.form['JoinDate']
        rowcount = db.create_member(first_name, last_name, email, phone_number, gender, birthday, baptism_status,
                                  join_date)
        if rowcount == 1:

            row = db.recent_member()
            member_id = row['id']
            db.add_member_to_homegroup(homegroup_id, member_id)
            flash("Member {} Created!".format(member.first_name.data, member.last_name.data))
            return redirect(url_for('get_homegroup_members', homegroup_id = homegroup_id))

    return render_template('create_member.html', form=member, homegroup_id = homegroup_id)


#views all members in a homegroup
@app.route('/homegroup/members/<homegroup_id>')
@login_required
@requires_roles('homegroup_leader', 'admin')
def get_homegroup_members(homegroup_id):
    current_homegroup = db.find_homegroup(homegroup_id)
    return render_template('homegroup_members.html', homegroup = db.get_homegroup_members(homegroup_id), currentHomegroup = current_homegroup)


#edits member information
@app.route('/member/edit/<member_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('homegroup_leader', 'admin')
def edit_member(member_id):
    row = db.find_member(member_id)
    member_form = CreateMemberForm( first_name = row['first_name'],
                                last_name = row['last_name'],
                                email = row['email'],
                                phone_number = row['phone_number'],
                                gender = row['gender'],
                                baptism_status = row['baptism_status'])
    birthday_form= row['birthday']
    join_date_form = row['join_date']
    if request.method == "POST" and member_form.validate():
        first_name = member_form.first_name.data
        last_name = member_form.last_name.data
        email = member_form.email.data
        phone_number = member_form.phone_number.data
        gender = member_form.gender.data
        birthday = request.form['Birthday']
        baptism_status = member_form.baptism_status.data
        join_date = request.form['JoinDate']
        rowcount = db.edit_member(member_id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, join_date)
        if (rowcount == 1):
            flash("Member {} Updated!".format(member_form.first_name.data))
            return redirect(url_for('all_members'))

    return render_template('edit_member.html', form = member_form, bDay = birthday_form, joinDay = join_date_form)

#removes a member from a particular homegroup
@app.route('/homegroup/member/delete/<homegroup_id>/<member_id>', methods = ['GET', 'POST'])
@login_required
@requires_roles('homegroup_leader', 'admin')
def remove_member(homegroup_id, member_id):
    rowcount = db.remove_member(homegroup_id, member_id)
    if rowcount == 1:
        flash("Member Removed!")
    return redirect(url_for('get_homegroup_members', homegroup_id = homegroup_id))


########################## ADMIN FUNCTIONS ##############################################

#### Admin - Home Group ####
class CreateHomeGroupForm(FlaskForm):
    name = StringField('Name')
    location = StringField('Address')
    description = StringField('Description')
    latitude = StringField('Latitude')
    longitude = StringField('Longitude')
    submit = SubmitField('Save Home Group')

#displays admin home page
@app.route('/admin')
def admin_home():
    attendance_count = db.get_attendance_counts()
    print(attendance_count)
    return render_template('admin_home.html', attendance_count=attendance_count)

#create homegroup
@app.route('/homegroup/create', methods=['GET','POST'])
@login_required
@requires_roles('admin')
def create_homegroup():
    new_homegroup = CreateHomeGroupForm()

    if request.method == "POST" and new_homegroup.validate():
        name = new_homegroup.name.data
        location = new_homegroup.location.data
        description = new_homegroup.description.data
        latitude = new_homegroup.latitude.data
        longitude = new_homegroup.longitude.data
        rowcount = db.create_homegroup(name, location, description, latitude, longitude)

        if rowcount == 1:
            flash("Homegroup {} Created!".format(new_homegroup.name.data))
            return redirect(url_for('get_homegroups'))

    return render_template('create_homegroup.html', form=new_homegroup)


#shows all homegroups
@app.route('/homegroup/all')
@login_required
@requires_roles('admin')
def get_homegroups():
    return render_template('homegroup_list.html', homegroup_list = db.get_all_homegroups())

#### Admin - Member ###########

#shows all members
@app.route('/member/all')
@login_required
@requires_roles('admin')
def all_members():
    return render_template('all_members.html', members = db.get_all_members(),
                           inactiveMembers = db.get_all_inactive_members(), showInactive = False)

#creates a member
@app.route('/member/create', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create_member():
    member = CreateMemberForm()

    if member.validate_on_submit():
        first_name = member.first_name.data
        last_name = member.last_name.data
        email = member.email.data
        phone_number = member.phone_number.data
        gender = member.gender.data
        birthday = request.form['Birthday']
        baptism_status = member.baptism_status.data
        join_date = request.form['JoinDate']
        rowcount = db.create_member(first_name, last_name, email, phone_number, gender, birthday, baptism_status, join_date)

        if rowcount == 1:
            flash("Member {} Created!".format(member.first_name.data))
            return redirect(url_for('all_members'))

    return render_template('create_member.html', form = member)


#sets a member inactive in the system
@app.route('/member/delete/<member_id>', methods = ['GET', 'POST'])
@login_required
@requires_roles('admin')
def deactivate_member(member_id):
    rowcount = db.deactivate_member(member_id)
    print(db.find_member(member_id)[9])
    # if the member is not active
    if db.find_member(member_id)[9] == 0:
        flash("Member Deactivated!")
    return redirect(url_for('all_members'))

#sets a member active in the system
@app.route('/member/add/<member_id>', methods = ['GET', 'POST'])
@login_required
@requires_roles('admin')
def reactivate_member(member_id):
    rowcount = db.reactivate_member(member_id)
    print(db.find_member(member_id)[9])
    # if the member is not active
    if db.find_member(member_id)[9] == 0:
        flash("Member Reactivated!")
    return redirect(url_for('all_members'))

#### Admin - Admin ###########

#shows all members
@app.route('/admin/all')
@login_required
@requires_roles('admin')
def all_admin():
    return render_template('admin_profiles.html', admin = db.get_all_admin(),
                           inactiveAdmin = db.get_all_inactive_admin(), showInactive = False)




# Make this the last line in the file!
if __name__ == '__main__':
    app.run(debug=True)