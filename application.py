from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, RadioField, SubmitField
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



@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

# Make this the last line in the file!
if __name__ == '__main__':
    app.run(debug=True)