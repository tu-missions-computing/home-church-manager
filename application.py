from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import Length
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'


class AttendanceForm(FlaskForm):
    user_id = StringField('User Id', validators=[Length(min=1, max=40)])
    attendance = StringField('Attendance', validators=[Length(min=1, max=5)])

@app.before_request
def before():
    db.open_db_connection()


@app.teardown_request
def after(exception):
    db.close_db_connection()


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/attendance', methods=['GET', 'POST'])
def addAttendance():
    error = ""
    form = AttendanceForm(request.form)

    if request.method == 'POST':
        form.validate_on_submit()

        if form.validate_on_submit():
            return redirect(url_for('thank_you'))

    return render_template('add-attendance.html', form=form, message=error)


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

# Make this the last line in the file!
if __name__ == '__main__':
    app.run(debug=True)