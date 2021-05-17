"""Data models."""
from . import db
from flask_login import UserMixin

association_table = db.Table('user_roles',
                             db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                             db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                             )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    roles = db.relationship("Role", secondary=association_table)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required
    libel = db.Column(db.String(100), unique=True)


if __name__ == "__main__":

    print("Done!")
