from datetime import datetime
import enum

from flask_security import UserMixin, RoleMixin

from app import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic', enable_typechecks=False))

    def __str__(self):
        return self.email


class Parent(User):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))


class School(User):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_registration_number = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(100))
    major = db.Column(db.String(50))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    parent = db.relationship('Parent', backref=db.backref('Student', lazy='dynamic'))

    def __repr__(self):
        return 'Student Registration Number: {} |*| Name: {}'.format(self.student_registration_number, self.name)


class BillStatus(enum.Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_status = db.Column(db.Enum(BillStatus, name='bill_status', default=BillStatus.PENDING.value))
    total_bill = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    student = db.relationship('Student', backref=db.backref('Bill'), uselist=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    def __repr__(self):
        return '${} USD'.format(self.total_bill)
