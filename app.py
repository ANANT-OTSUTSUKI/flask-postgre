from flask import Flask,render_template,redirect,request,url_for,make_response
from flask_login import login_required,LoginManager,current_user,login_user,logout_user,UserMixin
from model import db,STAFF,REQ,db_conn
from model import bcrypt,salt
from admin import admin
from staff import staff
from user import user
import datetime
from flask_mail import *
from random import *

app = Flask(__name__)
app.secret_key="hello motto"
  
app.config['MAIL_SERVER']='smtp.mail.yahoo.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'anantyadav1006@yahoo.com'  
app.config['MAIL_PASSWORD'] = 'onbqbekdhysnxdhy'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

def reload_script(url:str)->str:
    return f'''
<script>
setTimeout(function() {{window.location.assign("{url}")}},1000);
</script>
'''

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/week3_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(staff,url_prefix='/staff')
app.register_blueprint(user,url_prefix='/user')



login_manager=LoginManager(app)
login_manager.login_view='index'

@login_manager.user_loader
def load_user(username):
    return STAFF.query.filter_by(username=username).first()

@app.errorhandler(404)
def not_found(error):
    return "PAGE NOT FOUND OR INVALID INPUT"+reload_script("/")

@app.errorhandler(405)
def not_found(error):
    return "METHOD NOT ALLOWED. GO BY PROCESS"+reload_script("/")

@app.errorhandler(500)
def internal_server(error):
    return "Internal server Error"+reload_script("/")

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')
    elif current_user.isadmin=='1':
        return redirect(url_for('admin'))
    elif current_user.isadmin=='0' and current_user.isapproved=='1':
        return redirect(url_for('staff'))
    elif current_user.isadmin=='0' and current_user.isapproved=='0':
        return redirect(url_for('user'))

@app.route('/auth', methods=['post'])
def auth():
    username=request.form['username']
    password=request.form['password']
    passwordbyte=password.encode('utf-8')

    staff = STAFF.query.filter_by(username=username).first()
    if staff:
        s_pw=bytes.fromhex(staff.password)
    
    if staff and bcrypt.checkpw(passwordbyte,s_pw):
        if staff.isadmin=='1':
            login_user(staff)
            conn=db_conn()
            cur=conn.cursor()
            cur.execute('''INSERT INTO logins(username,l_date,l_time) VALUES(%s,%s,%s)''',(staff.username,datetime.date.today(),datetime.datetime.now().time()))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('admin'))
        elif staff.isadmin=='0' and staff.isapproved=='1':
            login_user(staff)
            conn=db_conn()
            cur=conn.cursor()
            cur.execute('''INSERT INTO logins(username,l_date,l_time) VALUES(%s,%s,%s)''',(staff.username,datetime.date.today(),datetime.datetime.now().time()))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('staff'))
        elif staff.isadmin=='0' and staff.isapproved=='0':
            login_user(staff)
            conn=db_conn()
            cur=conn.cursor()
            cur.execute('''INSERT INTO logins(username,l_date,l_time) VALUES(%s,%s,%s)''',(staff.username,datetime.date.today(),datetime.datetime.now().time()))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('user'))
    else:
        return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    if current_user.isadmin != '1':
        return redirect(url_for('index'))
    conn = db_conn()
    cur =conn.cursor()
    cur.execute('''SELECT * FROM customers ORDER BY c_id''')
    c_data = cur.fetchall()
    cur.execute('''SELECT * FROM staffs ORDER BY s_id''')
    s_data=cur.fetchall()
    cur.execute('''SELECT * FROM transactions ORDER BY s_id''')
    t_data=cur.fetchall()
    cur.execute('''SELECT * FROM logins''')
    l_data=cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    return render_template('admin.html', current_user=current_user,c_data=c_data,s_data=s_data,t_data=t_data,l_data=l_data)


@app.route('/staff')
@login_required
def staff():
    if current_user.isadmin != '0' and current_user.isapproved != '1':
        return redirect(url_for('index'))
    
    conn = db_conn()
    cur =conn.cursor()
    cur.execute('''SELECT * FROM customers ORDER BY c_id''')
    c_data = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return render_template('staff.html',current_user=current_user,c_data=c_data)

@app.route('/user')
@login_required
def user():
    if current_user.isadmin != '0' and current_user.isapproved !='0':
        return redirect(url_for('index'))
    

    return render_template('user.html',current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/test')
def test():
    return render_template('otp-req.html')

@app.route('/otp-req', methods=['post'])
def otp_req():
    username=request.form['username']
    
    staff= STAFF.query.filter_by(username=username).first()
    if not staff:
        return 'Enter valid username'+reload_script("/test")
    elif staff:
        email=staff.email
        otp= randint(0,999999)
        rend=render_template('validate.html')
        resp=make_response(rend)
        resp.set_cookie(key='otp',value=str(otp),max_age=300)  
        resp.set_cookie(key='username',value=username,max_age=600)      
        msg=Message("OTP",sender="anantyadav1006@yahoo.com",recipients=[email])
        msg.body=str(otp)
        mail.send(msg)
        return resp

@app.route('/validate', methods=['post'])
def validate():
    otp=request.cookies.get(key='otp')
    user_otp=request.form['EnteredOTP']
    if int(otp)==int(user_otp):
        return render_template('change-password.html')
    return 'failed'+reload_script('/test')


@app.route('/change-password', methods=['post'])
def change_pwd():
    pwd=request.form['password']
    username=request.cookies.get(key='username')
    pw=pwd.encode('utf-8')
    hashpw=bcrypt.hashpw(pw,salt).hex()
    con=db_conn()
    cur=con.cursor()
    cur.execute('''UPDATE staffs SET password=%s WHERE username=%s''',(hashpw,username))
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
