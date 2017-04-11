from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, RadioField, SubmitField, IntegerField, DateField
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Email, Length, DataRequired, NumberRange, InputRequired, EqualTo
from wtforms.validators import Length
from wtforms import validators
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'



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


@app.route('/')
def index():
    if 'email' not in session.keys():
        return redirect(url_for('login'))
    else:
        role = session['role']
        if role == 'homegroup_leader':
            return redirect(url_for("homegroup", homegroup_id=session['homegroup_id']))
    return redirect(url_for('login'))

@app.route('/map')
def map():
    homegroups = db.get_all_homegroups()

    return render_template('map.html', homegroups = homegroups)


class LoginForm(FlaskForm):
    email = StringField('E-mail Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():

        role = db.check_valid_user(login_form.email.data, login_form.password.data)
        if not role:
            flash ('Invalid username or password')
        else:
            session.clear()
            session['email'] = login_form.email.data
            session['role'] = role
            session['name'] = db.find_member_info(session['email'])['first_name']
            if role == 'homegroup_leader':
                session['homegroup_id'] = db.find_user_homegroup(session['email'])
            flash('Logged in successfully as {}'.format(session['email']))
            return redirect(url_for('index'))

    return render_template('login.html', form = login_form)

@app.route('/logout')
def logout():
    email = session.pop('email', None)
    session.clear()
    flash('Logged out')
    return redirect(url_for('login'))


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


class CreatememberForm(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=2, max=30, message="First name is a required field")])
    last_name = StringField('Last Name', [validators.Length(min=2, max=30, message="Last name is a required field")])
    email = StringField('Email', [validators.Email("Please enter valid email")])
    phone_number = IntegerField('Phone Number', [validators.InputRequired(message="Please enter your phone number")])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    baptism_status = SelectField('Baptized?', choices=[('yes', 'Yes'), ('no', 'No')])
    submit = SubmitField('Save Member')


@app.route('/homegroup/create_member/<homegroup_id>', methods=['GET', 'POST'])
def create_new_member_for_homegroup(homegroup_id):
    member = CreatememberForm()
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


@app.route('/member/create', methods=['GET', 'POST'])
def create_member():
    member = CreatememberForm()

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

@app.route('/member/all')
def all_members():
    return render_template('all_members.html', members = db.get_all_members())

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




class CreateHomeGroupForm(FlaskForm):
    name = StringField('Name')
    location = StringField('Location')
    description = StringField('Description')
    submit = SubmitField('Save Home Group')



@app.route('/homegroup/edit/<homegroup_id>', methods=['GET', 'POST'])
def edit_homegroup(homegroup_id):
    row = db.find_homegroup(homegroup_id)
    hg_form = CreateHomeGroupForm( name = row['name'],
                                description = row['description'],
                                location = row['location'])
    if hg_form.validate_on_submit():
        rowcount = db.edit_homegroup(homegroup_id, hg_form.name.data, hg_form.description.data, hg_form.location.data)
        if (rowcount == 1):
            flash("Home Group updated!")
            return redirect(url_for('homegroup', homegroup_id = homegroup_id))

    return render_template('edit_homegroup.html', form = hg_form)



@app.route('/homegroup/member/delete/<homegroup_id>/<member_id>', methods = ['GET', 'POST'])
def remove_member(homegroup_id, member_id):
    rowcount = db.remove_member(homegroup_id, member_id)
    if rowcount == 1:
        flash("Member Removed!")
    return redirect(url_for('get_homegroup_members', homegroup_id = homegroup_id))





@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

@app.route('/homegroup/<homegroup_id>')
def homegroup(homegroup_id):
    homegroup = db.find_homegroup(homegroup_id)
    return render_template('homegroup.html', currentHomegroup=homegroup)

# Make this the last line in the file!
if __name__ == '__main__':
    app.run(debug=True)