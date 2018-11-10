from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from  sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from psql_settings import sqlalchemy_database_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
adb = SQLAlchemy(app)
 
class HowDidYouFindOut (adb.Model):
    __tablename__="how_did_you_find_out"
    id = adb.Column(adb.Integer, primary_key=True)
    how_did_you_find_out_name = adb.Column(adb.Text)

class MaritalStatus (adb.Model):
    __tablename__ = "marital_status"
    id = adb.Column(adb.Integer, primary_key=True)
    marital_status_name = adb.Column(adb.Text)

class Role (adb.Model):
    __tablename__ = "role"
    id = adb.Column(adb.Integer, primary_key=True)
    role = adb.Column(adb.Text)

    homegroup_persons = relationship("HomegroupPersonRole")

class Person (adb.Model):
    __tablename__ = "person"
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
    attributes = adb.Column(adb.JSON)

    attendances = relationship("Attendance")
    homegroup_roles = relationship("HomegroupPersonRole")

class Attribute (adb.Model):
    __tablename__= "attribute"
    id = adb.Column(adb.Integer, primary_key=True)
    model_name = adb.Column(adb.Text)
    name = adb.Column(adb.Text)
    data_type = adb.Column(adb.Text)

