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
    submit = SubmitField('Save User')


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

@app.route('/homegroup/users/<homegroupid>')
def get_homegroup_users(homegroupid):
    return render_template('homegroup_users.html', homegroup = db.get_homegroup_users(homegroupid))

@app.route('/user/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    row = db.find_user(user_id)
    user_form = CreateUserForm( first_name = row['first_name'],
                                last_name = row['last_name'],
                                email = row['email'])
    if user_form.validate_on_submit():
        rowcount = db.edit_user(user_id, user_form.first_name.data, user_form.last_name.data, user_form.email.data)
        if (rowcount == 1):
            flash("user updated!")
            return redirect(url_for('index'))

    return render_template('edit_user.html', form = user_form)




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





@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

# Make this the last line in the file!
if __name__ == '__main__':
    app.run(debug=True)