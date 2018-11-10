from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from  sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from psql_settings import sqlalchemy_database_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
adb = SQLAlchemy(app)
 
class Homegroup (adb.Model):
    __tablename__ = "homegroup"
    id = adb.Column( adb.Integer, primary_key=True)
    name = adb.Column(adb.Text)
    location = adb.Column(adb.Text)
    description = adb.Column(adb.Text)
    latitude = adb.Column(adb.Float(precision=8, scale=8))
    longitude = adb.Column(adb.Float(precision=8, scale=8))
    creation_date = adb.Column(adb.Text)
    deactivation_date = adb.Column(adb.Text)

    attendances = relationship("Attendance")
    member_roles = relationship("HomegroupMemberRole")

class HowDidYouFindOut (adb.Model):
    __tablename__="how_did_you_find_out"
    id = adb.Column(adb.Integer, primary_key=True)
    how_did_you_find_out_name = adb.Column(adb.Text)

class MaritalStatus (adb.Model):
    __tablename__ = "marital_status"
    id = adb.Column(adb.Integer, primary_key=True)
    marital_status_name = adb.Column(adb.Text)

class Meeting (adb.Model):
    __tablename__ = "meeting"
    id = adb.Column(adb.Integer, primary_key=True)
    date = adb.Column(adb.Text)
    time = adb.Column(adb.Text)

    attendances = relationship("Attendance")

class Role (adb.Model):
    __tablename__ = "role"
    id = adb.Column(adb.Integer, primary_key=True)
    role = adb.Column(adb.Text)

    homegroup_members = relationship("HomegroupMemberRole")

class Member (adb.Model):
    __tablename__ = "member"
    id = adb.Column(adb.Integer, primary_key=True)
    first_name = adb.Column(adb.Text)
    last_name = adb.Column(adb.Text)
    email = adb.Column(adb.Text)
    phone_number = adb.Column(adb.Text)
    gender = adb.Column(adb.Text)
    birthday = adb.Column(adb.Text)
    password = adb.Column(adb.Text)
    baptism_status = adb.Column(adb.Boolean)
    marital_status_id = adb.Column(adb.Integer, ForeignKey('marital_status.id'))
    how_did_you_find_out_id = adb.Column(adb.Integer, ForeignKey('how_did_you_find_out.id'))
    is_a_parent = adb.Column(adb.Boolean)
    join_date = adb.Column(adb.Text)
    deactivation_date = adb.Column(adb.Text)

    attendances = relationship("Attendance")
    homegroup_roles = relationship("HomegroupMemberRole")

class Attendance (adb.Model):
    __tablename__ = "attendance"
    homegroup_id = adb.Column(adb.Integer, ForeignKey('homegroup.id'), primary_key=True)
    member_id = adb.Column(adb.Integer, ForeignKey('member.id'), primary_key = True)
    meeting_id = adb.Column(adb.Integer, ForeignKey('meeting.id'), primary_key = True)
    attendance = adb.Column(adb.Boolean)

class HomegroupMemberRole (adb.Model):
    __tablename__ = "homegroup_member_role"
    id = adb.Column(adb.Integer, primary_key=True)
    homegroup_id = adb.Column(adb.Integer, ForeignKey('homegroup.id'))
    member_id = adb.Column(adb.Integer, ForeignKey('member.id'))
    role_id = adb.Column(adb.Integer, ForeignKey('role.id'))
    creation_date = adb.Column(adb.Text)
    deactivation_date = adb.Column(adb.Text)

    homegroup = relationship('Homegroup')
    member = relationship('Member')
    role = relationship('Role')
