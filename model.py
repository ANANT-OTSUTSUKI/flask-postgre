from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt
import os

# Initialize SQLAlchemy WITHOUT app (important)
db = SQLAlchemy()

# bcrypt salt (ok to keep global)
salt = bcrypt.gensalt()

# =========================
# MODELS
# =========================

class STAFF(UserMixin, db.Model):
    __tablename__ = 'staffs'

    s_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    isadmin = db.Column(db.String)
    isapproved = db.Column(db.String)

    def get_id(self):
        return str(self.s_id)


class Customer(db.Model):
    __tablename__ = 'customers'

    c_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(200), unique=True, nullable=False)
    address = db.Column(db.String(500))


class REQ(db.Model):
    __tablename__ = 'req_approval'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)


class REP(db.Model):
    __tablename__ = 'req_admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)


class Trans(db.Model):
    __tablename__ = 'transactions'

    t_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, nullable=False)
    s_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    t_date = db.Column(db.String)
    t_time = db.Column(db.String)
