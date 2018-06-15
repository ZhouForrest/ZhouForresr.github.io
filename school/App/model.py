from datetime import datetime
from functools import wraps

from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Students(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(20))
    s_age = db.Column(db.Integer)
    s_bir = db.Column(db.DateTime, default=datetime.now)
    s_icon = db.Column(db.String(200))
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.g_id'), nullable=True)

    __tablename__ = 'students'

    def save(self):
        db.session.add(self)
        db.session.commit()


class Grades(db.Model):
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(20))
    students = db.relationship('Students', backref='grades', lazy=True)

    __tablename__ = 'grades'

    def save(self):
        db.session.add(self)
        db.session.commit()


class Users(db.Model):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    u_name = db.Column(db.String(20))
    u_password = db.Column(db.String(16))
    u_icon = db.Column(db.String(200))

    __tablename__ = 'users'

    def save(self):
        db.session.add(self)
        db.session.commit()


sc = db.Table('sc',
              db.Column('s_id', db.Integer, db.ForeignKey('students.s_id'), primary_key=True),
              db.Column('g_id', db.Integer, db.ForeignKey('course.c_id'), primary_key=True))


class Course(db.Model):
    c_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    c_name = db.Column(db.String(20))
    c_score = db.Column(db.Integer, default=0)
    student = db.relationship('Students', secondary=sc, backref=db.backref('course', lazy=True))


    __tablename = 'course'

    def save(self):
        db.session.add(self)
        db.session.commit()


def is_login(func):
    @wraps(func)
    def check_login():
        user_session = session.get('u_id')
        if user_session:
            return func()
        else:
            return redirect(url_for('user.login'))
    return check_login