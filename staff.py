from flask import Blueprint,request,Flask,render_template,redirect,url_for
from flask_login import login_required,current_user,login_user,logout_user,UserMixin
from model import db,REQ,db_conn,REP,Customer,Trans
staff = Blueprint('staff',__name__,template_folder='templates')
import datetime


@staff.route('/create-customer', methods=['post'])
@login_required
def create_customer():
    name = request.form['name']
    mail = request.form['mail']
    address = request.form['address']

    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''INSERT INTO customers(name,mail,address) VALUES(%s,%s,%s);''',(name,mail,address))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('staff'))
@staff.route('/upc',methods=['post'])
@login_required
def upc():
    c_id = request.form['c_id']
    customer=Customer.query.filter_by(c_id=c_id).first()
    if not customer:
        return 'Enter Valid Customer ID'
    conn= db_conn()
    cur=conn.cursor()
    cur.execute('''SELECT * FROM customers WHERE c_id=%s''',(c_id))
    data=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('upc.html',data=data)

@staff.route('/update-customer',methods=['post'])
@login_required
def update_customer():
    c_id=request.form['c_id']
    name = request.form['name']
    mail = request.form['mail']
    address = request.form['address']
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''UPDATE customers SET (name,mail,address)=(%s,%s,%s) WHERE c_id = %s''',(name,mail,address,c_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('staff'))

@staff.route('/delete-customer',methods=['post'])
@login_required
def delete_customer():
    c_id=request.form['c_id']
    customer=Customer.query.filter_by(c_id=c_id).first()
    if not customer:
        return 'Enter Valid Customer ID'
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''DELETE FROM customers where c_id=%s''',(c_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('staff'))


@staff.route('/request-approval', methods=['post'])
@login_required
def req_admin():
    s_id = request.form['s_id']
    req = REP.query.filter_by(s_id=s_id).first()
    if req:
        return 'APPROVAL IS ALREADY IN PROCESS'
    else:
        conn = db_conn()
        cur=conn.cursor()
        cur.execute('''SELECT username FROM staffs WHERE s_id=%s''',(s_id))
        username = cur.fetchone()
        cur.execute('''INSERT INTO req_admin(s_id,username) VALUES(%s,%s)''',(s_id,username))
        conn.commit()
        cur.close()
        conn.close()

        return 'APPROVAL REQUESTED'
    
@staff.route('/add-transaction', methods=['post'])
@login_required
def add_trans():
    c_id=request.form['c_id']
    s_id=request.form['s_id']
    amount=request.form['amount']

    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''INSERT INTO transactions(c_id,s_id,amount,t_date,t_time) VALUES(%s,%s,%s,%s,%s)''',(c_id,s_id,amount,datetime.date.today(),datetime.datetime.now().time()))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('staff'))
    

@staff.route('/upt',methods=['post'])
@login_required
def upt():
    t_id = request.form['t_id']
    trans=Trans.query.filter_by(t_id=t_id).first()
    if not trans:
        return 'Enter Valid Transaction ID'
    conn= db_conn()
    cur=conn.cursor()
    cur.execute('''SELECT * FROM transactions WHERE t_id=%s''',(t_id))
    data=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('upt.html',data=data)

@staff.route('/update-transaction',methods=['post'])
@login_required
def update_trans():
    t_id=request.form['t_id']
    s_id = request.form['s_id']
    c_id = request.form['c_id']
    amount = request.form['amount']
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''UPDATE transactions SET (s_id,c_id,amount,t_time,t_date)=(%s,%s,%s,%s,%s) WHERE t_id = %s''',(s_id,c_id,amount,datetime.datetime.now().time(),datetime.date.today(),t_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('staff'))

@staff.route('/delete-transaction',methods=['post'])
@login_required
def delete_trans():
    t_id=request.form['t_id']
    transaction=Trans.query.filter_by(t_id=t_id).first()
    if not transaction:
        return 'Enter Valid transaction ID'
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''DELETE FROM transactions where t_id=%s''',(t_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('staff'))