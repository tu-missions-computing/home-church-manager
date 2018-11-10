from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from  sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from psql_settings import sqlalchemy_database_uri
from base_models import *

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
    attributes = adb.Column(adb.JSON)

    attendances = relationship("Attendance")
    person_roles = relationship("HomegroupPersonRole")

class Meeting (adb.Model):
    __tablename__ = "meeting"
    id = adb.Column(adb.Integer, primary_key=True)
    date = adb.Column(adb.Text)
    time = adb.Column(adb.Text)

    attendances = relationship("Attendance")

class Attendance (adb.Model):
    __tablename__ = "attendance"
    homegroup_id = adb.Column(adb.Integer, ForeignKey('homegroup.id'), primary_key=True)
    person_id = adb.Column(adb.Integer, ForeignKey('person.id'), primary_key = True)
    meeting_id = adb.Column(adb.Integer, ForeignKey('meeting.id'), primary_key = True)
    attendance = adb.Column(adb.Boolean)

class HomegroupPersonRole (adb.Model):
    __tablename__ = "homegroup_person_role"
    id = adb.Column(adb.Integer, primary_key=True)
    homegroup_id = adb.Column(adb.Integer, ForeignKey('homegroup.id'))
    person_id = adb.Column(adb.Integer, ForeignKey('person.id'))
    role_id = adb.Column(adb.Integer, ForeignKey('role.id'))
    creation_date = adb.Column(adb.Text)
    deactivation_date = adb.Column(adb.Text)

    homegroup = relationship('Homegroup')
    person = relationship('Person')
    role = relationship('Role')

