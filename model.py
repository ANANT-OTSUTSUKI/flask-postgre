from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import psycopg2
import bcrypt

salt=bcrypt.gensalt()

def db_conn():
    conn = psycopg2.connect(database = "week3_db", host="localhost", user="postgres", password="12345678", port="5432")
    return conn


db = SQLAlchemy()

class STAFF(UserMixin,db.Model):
    __tablename__ = 'staffs'
    s_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique = True)
    email=db.Column(db.String(200), unique = True)
    password = db.Column(db.String(1000))
    isadmin=db.Column(db.String)
    isapproved=db.Column(db.String)

   

    def get_id(self):
        return self.username
    def __init__(self, username):
        self.username = username


class Customer(db.Model):
    __tablename__ = 'customers'
    c_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    mail=db.Column(db.String(200), unique = True)
    address=db.Column(db.String(500))
    
    def get_id(self):
        return self.username
    def __init__(self, username):
        self.username = username

class REQ(db.Model):
    __tablename__ = 'req_approval'
    s_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
   
    def get_id(self):
        return self.username
    def __init__(self, username):
        self.username = username


class REP(db.Model):
    __tablename__ = 'req_admin'
    s_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
   
    def get_id(self):
        return self.username
    def __init__(self, username):
        self.username = username

        
class Trans(UserMixin,db.Model):
    __tablename__ = 'transactions'
    t_id=db.Column(db.Integer,primary_key=True)
    c_id=db.Column(db.Integer)
    s_id=db.Column(db.Integer)
    amount=db.Column(db.Integer)
    t_date=db.Column(db.String)
    t_time=db.Column(db.String)

   

    def get_id(self):
        return self.t_id
    def __init__(self, t_id):
        self.t_id = t_id
