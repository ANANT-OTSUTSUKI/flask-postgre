import psycopg2
from model import bcrypt,salt
pwd1='iamadmin'
pwd2='user'
pwd3='staff'

b1=pwd1.encode('utf-8')
b2=pwd2.encode('utf-8')
b3=pwd3.encode('utf-8')

hash1=bcrypt.hashpw(b1,salt).hex()
hash2=bcrypt.hashpw(b2,salt).hex()
hash3=bcrypt.hashpw(b3,salt).hex()

conn = psycopg2.connect(database = "week3_db", host="localhost", user="postgres", password="12345678", port="5432")

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS staffs(s_id serial primary key,username varchar(100) UNIQUE,email varchar(200) UNIQUE,password varchar(1000),isadmin bit,isapproved bit);''')
cur.execute('''INSERT INTO staffs(username,email,password,isadmin,isapproved) VALUES('anant','anantweek3.dsoc@yahoo.com',%s,'1','1'),('john','john@gmail.com',%s,'0','0'),('staff','staff@gmail.com',%s,'0','1');''',(hash1,hash2,hash3))

cur.execute('''CREATE TABLE IF NOT EXISTS customers(c_id serial primary key, name varchar(100), mail varchar(200) UNIQUE, address varchar(500));''')
cur.execute('''INSERT INTO customers(name,mail,address) VALUES('Peru','peru@gmail.com','Rohini'),('Sarah','sarah123@hotmail.com','Dwarka');''')

cur.execute('''CREATE TABLE IF NOT EXISTS transactions(t_id serial primary key, c_id integer , s_id integer, amount integer,t_date DATE,t_time TIME, FOREIGN KEY (c_id) REFERENCES customers(c_id), FOREIGN KEY (s_id) REFERENCES staffs(s_id));''')
cur.execute('''INSERT INTO transactions(c_id,s_id,amount,t_date,t_time) VALUES(2,1,1500,'2024-12-17','19:33:25.0117');''')

cur.execute('''CREATE TABLE IF NOT EXISTS req_approval(s_id integer primary key  UNIQUE,username varchar(100));''')
cur.execute('''CREATE TABLE IF NOT EXISTS req_admin(s_id integer primary key  UNIQUE,username varchar(100));''')

cur.execute('''CREATE TABLE IF NOT EXISTS logins(username varchar(100),l_date DATE,l_time TIME)''')
conn.commit()
cur.close()
conn.close()