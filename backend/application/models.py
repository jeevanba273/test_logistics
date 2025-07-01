from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from application.database import db

# Define models
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    delivery_date = db.Column(db.String(100), default='to be updated')
    source_city = db.Column(db.String(255), nullable=False)
    destination_city = db.Column(db.String(255), nullable=False)
    internal_status = db.Column(db.String(100), default='requested')
    delivery_status = db.Column(db.String(100), default='processing')
    description = db.Column(db.Text)
    amount = db.Column(db.Float, default=0.0)
    
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))