from flask import Blueprint,request,Flask,render_template,redirect,url_for
from flask_login import login_required,current_user,login_user,logout_user,UserMixin
from model import db,REQ,db_conn
user = Blueprint('user',__name__,template_folder='templates')



@user.route('/request-approval', methods=['post'])
@login_required
def req_approval():
    s_id = request.form['s_id']
    req = REQ.query.filter_by(s_id=s_id).first()
    if req:
        return 'APPROVAL IS IN PROCESS'
    else:
        conn = db_conn()
        cur=conn.cursor()
        cur.execute('''SELECT username FROM staffs WHERE s_id=%s''',(s_id))
        username = cur.fetchone()
        cur.execute('''INSERT INTO req_approval(s_id,username) VALUES(%s,%s)''',(s_id,username))
        conn.commit()
        cur.close()
        conn.close()

        return 'APPROVAL REQUESTED'
