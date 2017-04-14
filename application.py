from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, RadioField, SubmitField, IntegerField, DateField
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Email, Length, DataRequired, NumberRange, InputRequired, EqualTo
from wtforms.validators import Length
from wtforms import validators




import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'


login_mgr = LoginManager()
login_mgr = LoginManager(app)

class AttendanceForm(FlaskForm):
    # member_id = StringField('member Id', validators=[Length(min=1, max=40)])
    # meeting_id = StringField('Meeting Id', validators=[Length(min=1, max=40)])
    radio = RadioField('Attendance', choices=["y","n"])
    submit = SubmitField('Submit')

@app.before_request
def before():
    db.open_db_connection()


@app.teardown_request
def after(exception):
    db.close_db_connection()


########################## INDEX + MAP ##############################################

@app.route('/')
def index():
   User = load_user(session['username'])
   print(User.role);
# return redirect(url_for("homegroup", homegroup_id=session['homegroup_id']))
   return redirect(url_for('login'))

@app.route('/map')
def map():
    homegroups = db.get_all_homegroups()

    return render_template('map.html', homegroups = homegroups)


########################## USER + LOGIN ##############################################
class UserForm(FlaskForm):
    email = StringField('E-mail Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create User')

@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    user_form = UserForm()
    if user_form.validate_on_submit():
        pw_hash = user_form.password.data
        db.create_user(user_form.email.data, pw_hash, 1)
        flash('User Created')
        return redirect(url_for('index'))
    return render_template('create_user.html', form=user_form)

class User(object):
    """Class for the currently logged-in user (if there is one). Only stores the user's e-mail."""
    def __init__(self, email):
        self.email = email
        self.role = db.find_user(self.email)['role']
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

def authenticate(email, password):
    """Check whether the arguments match a user from the "database" of valid users."""
    valid_users = db.get_all_users()
    for user in valid_users:
        if email == user['email'] and password == user['password']:
            return email
    return None

class LoginForm(FlaskForm):
    email = StringField('E-mail Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        if authenticate(login_form.email.data, login_form.password.data):
            # Credentials authenticated.
            # Create the user object, let Flask-Login know, and redirect to the home page
            user = User(login_form.email.data)
            login_user(user)
            session['username'] = login_form.email.data
            flash('Logged in successfully as {}'.format(login_form.email.data))
            return redirect(url_for('index'))
        else:
            # Authentication failed.
            flash('Invalid email address or password')
            return redirect(url_for('index'))

    return render_template('login.html', form = login_form)

@app.route('/logout')
def logout():
    logout_user()
    user_name = session.pop('username', None)
    flash('Logged out')
    return redirect(url_for('index'))

########################## HOME GROUP  (Home Group Leader)##############################################



@app.route('/homegroup/attendance/<homegroup_id>', methods=['GET', 'POST'])
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

@app.route('/homegroup/attendance/add/<homegroup_id>/<member_id>/<meeting_id>/<attendance>')
def updateAttendance(homegroup_id, member_id, attendance, meeting_id ):
    db.update_attendance(homegroup_id, member_id, meeting_id, attendance)
    return redirect(url_for('edit_attendance', homegroup_id=homegroup_id, meeting_id=meeting_id))


@app.route('/homegroup/attendance/edit/<homegroup_id>/<meeting_id>')
def edit_attendance(homegroup_id, meeting_id):
    members = db.get_attendance(homegroup_id, meeting_id)
    date = db.find_date(meeting_id)['date']
    time = db.find_date(meeting_id)['time']
    return render_template('edit_attendance.html', currentHomegroup = homegroup_id, meeting_id = meeting_id, members = members, date = date, time = time)



@app.route('/homegroup/attendance/dates/<homegroup_id>', methods=['GET'])
def get_attendance_dates(homegroup_id):
    return render_template('attendance_reports.html', currentHomegroup=homegroup_id, records=db.get_attendance_dates(homegroup_id))

@app.route('/homegroup/edit/<homegroup_id>', methods=['GET', 'POST'])
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
            return redirect(url_for('get_homegroups'))

    return render_template('edit_homegroup.html', form = hg_form)

@app.route('/homegroup/<homegroup_id>')
def homegroup(homegroup_id):
    homegroup = db.find_homegroup(homegroup_id)
    return render_template('homegroup.html', currentHomegroup=homegroup)

@app.route('/homegroup/select_location')
def select_location():
    return render_template('select_location.html')


########################## MEMBER (Home Group Leader) ##############################################


class CreateMemberForm(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=2, max=30, message="First name is a required field")])
    last_name = StringField('Last Name', [validators.Length(min=2, max=30, message="Last name is a required field")])
    email = StringField('Email', [validators.Email("Please enter valid email")])
    phone_number = IntegerField('Phone Number', [validators.InputRequired(message="Please enter valid phone number")])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    baptism_status = SelectField('Baptized?', choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Save Member')


@app.route('/homegroup/create_member/<homegroup_id>', methods=['GET', 'POST'])
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





@app.route('/homegroup/members/<homegroup_id>')
def get_homegroup_members(homegroup_id):
    current_homegroup = db.find_homegroup(homegroup_id)
    return render_template('homegroup_members.html', homegroup = db.get_homegroup_members(homegroup_id), currentHomegroup = current_homegroup)

@app.route('/member/edit/<member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    row = db.find_member(member_id)
    member_form = CreatememberForm( first_name = row['first_name'],
                                last_name = row['last_name'],
                                email = row['email'],
                                phone_number = row['phone_number'],
                                gender = row['gender'],
                                baptism_status = row['baptism_status'])
    birthday_form = row['birthday']
    join_date_form = row['join_date']
    if request.method == "POST":
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
            return redirect(url_for('get_homegroup_members', homegroup_id = 1))

    return render_template('edit_member.html', form = member_form, bDay = birthday_form, joinDay = join_date_form)


@app.route('/homegroup/member/delete/<homegroup_id>/<member_id>', methods = ['GET', 'POST'])
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

@app.route('/homegroup/create', methods=['GET','POST'])
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

@app.route('/homegroup/all')
def get_homegroups():
    return render_template('homegroup_list.html', homegroup_list = db.get_all_homegroups())

#### Admin - Member ####
@app.route('/member/all')
def all_members():
    return render_template('all_members.html', members = db.get_all_members())


@app.route('/member/create', methods=['GET', 'POST'])
def create_member():
    member = CreateMemberForm()

    if member.validate_on_submit():
        first_name = member.first_name.data
        last_name = member.last_name.data
        email = member.email.data
        phone_number = member.phone_number.data
        gender = member.gender.data
        birthday = member.birthday.data
        baptism_status = member.baptism_status.data
        join_date = member.join_date.data
        rowcount = db.create_member(first_name, last_name, email, phone_number, gender, birthday, baptism_status, join_date)

        if rowcount == 1:
            flash("Member {} Created!".format(member.first_name.data))
            return redirect(url_for('all_members'))

    return render_template('create_member.html', form = member)



@app.route('/member/delete/<member_id>', methods = ['GET', 'POST'])
def deactivate_member(member_id):
    rowcount = db.deactivate_member(member_id)
    print(db.find_member(member_id)[9])
    # if the member is not active
    if db.find_member(member_id)[9] == 0:
        flash("Member Deactivated!")
    return redirect(url_for('all_members'))





# Make this the last line in the file!
if __name__ == '__main__':
    app.run(debug=True)