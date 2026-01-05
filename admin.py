from flask import Blueprint,request,Flask,render_template,redirect,url_for
from flask_login import login_required,current_user,login_user,logout_user,UserMixin
from model import db,REQ,db_conn,REP,bcrypt,salt,STAFF,Customer,Trans
import datetime
admin = Blueprint('admin',__name__,template_folder='templates')

@admin.route('/req-admin')
@login_required
def req_admin_app():
    rep = REP.query.count()
    if rep==0:
        return 'No Requests Right Now'
    else:
        conn = db_conn()
        cur=conn.cursor()
        cur.execute('''SELECT * FROM req_admin;''')
        data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return render_template('admin-update.html',data=data)


@admin.route('/req-approval-acc', methods=['post'])
@login_required
def req_app_accept():
    s_id = request.form['s_id']
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''UPDATE staffs SET isadmin='1' WHERE s_id=%s''',(s_id))
    cur.execute('''DELETE FROM req_admin WHERE s_id=%s''',(s_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin.req_admin_app'))

@admin.route('/req-approval-rej', methods=['post'])
@login_required
def req_app_reject():
    s_id = request.form['s_id']
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''DELETE FROM req_admin WHERE s_id=%s''',(s_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin.req_admin_app'))


@admin.route('/req-staff')
@login_required
def req_approval_app():
    rep = REQ.query.count()
    if rep==0:
        return 'No Requests Right Now'
    else:
        conn = db_conn()
        cur=conn.cursor()
        cur.execute('''SELECT * FROM req_approval;''')
        data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return render_template('staff-update.html',data=data)


@admin.route('/req-approval-acc-s', methods=['post'])
@login_required
def req_app_accept_s():
    s_id = request.form['s_id']
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''UPDATE staffs SET isapproved='1' WHERE s_id=%s''',(s_id))
    cur.execute('''DELETE FROM req_approval WHERE s_id=%s''',(s_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin.req_approval_app'))

@admin.route('/req-approval-rej-s', methods=['post'])
@login_required
def req_app_reject_s():
    s_id = request.form['s_id']
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''DELETE FROM req_admin WHERE s_id=%s''',(s_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin.req_approval_app'))




@admin.route('/create-customer', methods=['post'])
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
    return redirect(url_for('admin'))
@admin.route('/upc',methods=['post'])
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
    return render_template('upcs.html',data=data)

@admin.route('/update-customer',methods=['post'])
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
    return redirect(url_for('admin'))

@admin.route('/delete-customer',methods=['post'])
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
    return redirect(url_for('admin'))



@admin.route('/create-staff', methods=['post'])
@login_required
def create_staff():
    name = request.form['username']
    mail = request.form['email']
    password = request.form['password']
    pwd=password.encode('utf-8')
    hashpwd=bcrypt.hashpw(pwd,salt).hex()
    isadmin=request.form['isadmin']
    isapproved=request.form['isapproved']

    if isadmin=='1' and isapproved=='0':
        return 'If staff you want to add is admin, it should be approved too.'

    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''INSERT INTO staffs(username,email,password,isadmin,isapproved) VALUES(%s,%s,%s,%s,%s);''',(name,mail,hashpwd,isadmin,isapproved))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin'))
@admin.route('/upca',methods=['post'])
@login_required
def upca():
    s_id = request.form['s_id']
    staff=STAFF.query.filter_by(s_id=s_id).first()
    if not staff:
        return 'Enter Valid Staff ID'
    
    conn= db_conn()
    cur=conn.cursor()
    cur.execute('''SELECT * FROM staffs WHERE s_id=%s''',(s_id))
    data=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('upcas.html',data=data)

@admin.route('/update-staff',methods=['post'])
@login_required
def update_staff():
    s_id=request.form['s_id']
    name = request.form['name']
    mail = request.form['mail']
    isadmin = request.form['isadmin']
    isapproved=request.form['isapproved']
    conn=db_conn()
    cur=conn.cursor()
    cur.execute('''UPDATE staffs SET (username,email,isadmin,isapproved)=(%s,%s,%s,%s) WHERE s_id = %s''',(name,mail,isadmin,isapproved,s_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin'))

@admin.route('/delete-staff',methods=['post'])
@login_required
def delete_staff():
    s_id=request.form['s_id']
    staff=STAFF.query.filter_by(s_id=s_id).first()
    if not staff:
        return 'Enter Valid Staff ID'
    conn=db_conn()
    cur=conn.cursor()

    cur.execute('''DELETE FROM staffs where s_id=%s''',(s_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin'))

@admin.route('/add-transaction', methods=['post'])
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
    return redirect(url_for('admin'))

@admin.route('/upta',methods=['post'])
@login_required
def upta():
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
    return render_template('upta.html',data=data)

@admin.route('/update-transaction',methods=['post'])
@login_required
def update_tran():
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
    return redirect(url_for('admin'))

@admin.route('/delete-transaction',methods=['post'])
@login_required
def delete_tran():
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
    return redirect(url_for('admin'))