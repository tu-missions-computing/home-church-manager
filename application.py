from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, RadioField, SubmitField, IntegerField, DateField
from wtforms import StringField, SubmitField, SelectField, FloatField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Email, Length, DataRequired, NumberRange, InputRequired, EqualTo
from wtforms.validators import Length
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'


class AttendanceForm(FlaskForm):
    # user_id = StringField('User Id', validators=[Length(min=1, max=40)])
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
    return redirect(url_for("homegroup", homegroup_id=1))
@app.route('/members')
def trip_report():
    return render_template('users.html', report = db.get_users())


@app.route('/homegroup/attendance/<homegroup_id>', methods=['GET', 'POST'])
def attendance(homegroup_id):
    error = ""
    attendance_form = AttendanceForm()
    users = db.get_homegroup_users(homegroup_id)
    show_users = 'N'
    if (request.method == "POST"):

        date = request.form['AttendanceDate']
        time = request.form['AttendanceTime']
        show_users = 'Y'
        meeting_id = db.add_date(date, time)['id']
        db.generate_attendance_report(homegroup_id, meeting_id)
        users = db.get_attendance(homegroup_id, meeting_id)
        return render_template('attendance.html', meeting_id = meeting_id, currentHomegroup=homegroup_id, form=attendance_form, users=users,showusers=show_users, date = date, time=time)

    return render_template('attendance.html', currentHomegroup = homegroup_id, form=attendance_form, users=users, showusers = show_users)

@app.route('/homegroup/attendance/add/<homegroup_id>/<user_id>/<meeting_id>/<attendance>')
def updateAttendance(homegroup_id, user_id, attendance, meeting_id ):
    attendance_form = AttendanceForm()
    db.update_attendance(homegroup_id, user_id, meeting_id, attendance)
    users = db.get_attendance(homegroup_id, meeting_id)
    show_users = 'Y'
    date = db.find_date(meeting_id)['date']
    time = db.find_date(meeting_id)['time']
    return render_template('attendance.html', currentHomegroup = homegroup_id, form = attendance_form, meeting_id = meeting_id, users = users, showusers = show_users, date = date, time = time)


@app.route('/homegroup/attendance/edit/<homegroup_id>/<meeting_id>')
def edit_attendance(homegroup_id, meeting_id):
    users = db.get_attendance(homegroup_id, meeting_id)
    show_users = 'Y'
    date = db.find_date(meeting_id)['date']
    time = db.find_date(meeting_id)['time']
    return render_template('attendance.html', currentHomegroup = homegroup_id, meeting_id = meeting_id, users = users, showusers = show_users, date = date, time = time)



@app.route('/homegroup/attendance/dates/<homegroup_id>', methods=['GET'])
def get_attendance_dates(homegroup_id):
    return render_template('attendance_reports.html', currentHomegroup=homegroup_id, records=db.get_attendance_dates(homegroup_id))


class CreateUserForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    phone_number = IntegerField('Phone Number')
    gender = SelectField('Gender', choices=[('male','Male'),('female','Female')])
    baptism_status = SelectField('Baptized?', choices=[('yes','Yes'),('no','No')])
    submit = SubmitField('Save User')


@app.route('/homegroup/create_user/<homegroup_id>', methods=['GET', 'POST'])
def create_new_user_for_homegroup(homegroup_id):
    user = CreateUserForm()
    if request.method == "POST":
        first_name = user.first_name.data
        last_name = user.last_name.data
        email = user.email.data
        phone_number = user.phone_number.data
        gender = user.gender.data
        birthday = request.form['Birthday']
        baptism_status = user.baptism_status.data
        join_date = request.form['JoinDate']
        rowcount = db.create_user(first_name, last_name, email, phone_number, gender, birthday, baptism_status,
                                  join_date)
        if rowcount == 1:

            row = db.recent_user()
            user_id = row['id']
            db.add_user_to_homegroup(homegroup_id, user_id)
            flash("User {} created!".format(user.first_name.data))
            return redirect(url_for('get_homegroup_users', homegroup_id = homegroup_id))

    return render_template('create_user.html', form=user, homegroup_id = homegroup_id)


@app.route('/member/create', methods=['GET', 'POST'])
def create_user():
    user = CreateUserForm()

    if user.validate_on_submit():
        first_name = user.first_name.data
        last_name = user.last_name.data
        email = user.email.data
        phone_number = user.phone_number.data
        gender = user.gender.data
        birthday = user.birthday.data
        baptism_status = user.baptism_status.data
        join_date = user.join_date.data
        rowcount = db.create_user(first_name, last_name, email, phone_number, gender, birthday, baptism_status, join_date)

        if rowcount == 1:
            flash("User {} created!".format(user.first_name.data))
            return redirect(url_for('all_users'))

    return render_template('create_user.html', form = user)

@app.route('/member/all')
def all_users():
    return render_template('all_users.html', users = db.get_all_users())

@app.route('/homegroup/members/<homegroup_id>')
def get_homegroup_users(homegroup_id):
    current_homegroup = db.find_homegroup(homegroup_id)
    return render_template('homegroup_users.html', homegroup = db.get_homegroup_users(homegroup_id), currentHomegroup = current_homegroup)

@app.route('/user/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    row = db.find_user(user_id)
    user_form = CreateUserForm( first_name = row['first_name'],
                                last_name = row['last_name'],
                                email = row['email'],
                                phone_number = row['phone_number'],
                                gender = row['gender'],
                                baptism_status = row['baptism_status'])
    birthday_form = row['birthday']
    join_date_form = row['join_date']
    if request.method == "POST":
        first_name = user_form.first_name.data
        last_name = user_form.last_name.data
        email = user_form.email.data
        phone_number = user_form.phone_number.data
        gender = user_form.gender.data
        birthday = request.form['Birthday']
        baptism_status = user_form.baptism_status.data
        join_date = request.form['JoinDate']
        rowcount = db.edit_user(user_id, first_name, last_name, email, phone_number, gender, birthday, baptism_status, join_date)
        if (rowcount == 1):
            flash("user updated!")
            return redirect(url_for('get_homegroup_users', homegroup_id = 1))

    return render_template('edit_user.html', form = user_form, bDay = birthday_form, joinDay = join_date_form)




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
            return redirect(url_for('homegroup', id = homegroup_id))

    return render_template('edit_homegroup.html', form = hg_form)



@app.route('/homegroup/user/delete/<homegroup_id>/<user_id>', methods = ['GET', 'POST'])
def remove_user(homegroup_id, user_id):
    rowcount = db.remove_user(homegroup_id, user_id)
    if rowcount == 1:
         flash("User removed!")
    return redirect(url_for('get_homegroup_users', homegroup_id = homegroup_id))





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