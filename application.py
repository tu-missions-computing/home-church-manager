from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, RadioField, SubmitField
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
    return render_template('base.html')

@app.route('/users')
def trip_report():
    return render_template('users.html', report = db.get_users())


@app.route('/attendance', methods=['GET', 'POST'])
def addAttendance():
    error = ""
    form = AttendanceForm(request.form)
    users = db.get_users()

    if form.validate_on_submit():
        for i in range(1, db.get_user_count()):
            attendance = form.radio+i
        return redirect(url_for('thank_you'))

    return render_template('attendance.html', form=form, users=users)



class CreateUserForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    submit = SubmitField('Create User')


@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    user = CreateUserForm()

    if user.validate_on_submit():
        first_name = user.first_name.data
        last_name = user.last_name.data
        email = user.email.data
        rowcount = db.create_user(first_name, last_name, email)
        if rowcount == 1:
            flash("User {} created!".format(user.first_name.data))
            return redirect(url_for('all_users'))

    return render_template('create_user.html', form = user)

@app.route('/user/all')
def all_users():
    return render_template('all_users.html', users = db.get_all_users())


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

# Make this the last line in the file!
if __name__ == '__main__':
    app.run(debug=True)