from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from model import db, STAFF, Customer, Trans, REQ, REP
import datetime

admin = Blueprint('admin', __name__, template_folder='templates')

# =========================
# ADMIN REQUESTS
# =========================

@admin.route('/req-admin')
@login_required
def req_admin_app():
    data = REP.query.all()
    if not data:
        return 'No Requests Right Now'
    return render_template('admin-update.html', data=data)


@admin.route('/req-approval-acc', methods=['POST'])
@login_required
def req_app_accept():
    s_id = request.form['s_id']
    staff = STAFF.query.get(s_id)
    if staff:
        staff.isadmin = '1'
        REP.query.filter_by(s_id=s_id).delete()
        db.session.commit()
    return redirect(url_for('admin.req_admin_app'))


@admin.route('/req-approval-rej', methods=['POST'])
@login_required
def req_app_reject():
    s_id = request.form['s_id']
    REP.query.filter_by(s_id=s_id).delete()
    db.session.commit()
    return redirect(url_for('admin.req_admin_app'))


@admin.route('/req-staff')
@login_required
def req_approval_app():
    data = REQ.query.all()
    if not data:
        return 'No Requests Right Now'
    return render_template('staff-update.html', data=data)


@admin.route('/req-approval-acc-s', methods=['POST'])
@login_required
def req_app_accept_s():
    s_id = request.form['s_id']
    staff = STAFF.query.get(s_id)
    if staff:
        staff.isapproved = '1'
        REQ.query.filter_by(s_id=s_id).delete()
        db.session.commit()
    return redirect(url_for('admin.req_approval_app'))


@admin.route('/req-approval-rej-s', methods=['POST'])
@login_required
def req_app_reject_s():
    s_id = request.form['s_id']
    REQ.query.filter_by(s_id=s_id).delete()
    db.session.commit()
    return redirect(url_for('admin.req_approval_app'))

# =========================
# CUSTOMER MANAGEMENT
# =========================

@admin.route('/create-customer', methods=['POST'])
@login_required
def create_customer():
    customer = Customer(
        name=request.form['name'],
        mail=request.form['mail'],
        address=request.form['address']
    )
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for('admin.admin'))


@admin.route('/update-customer', methods=['POST'])
@login_required
def update_customer():
    customer = Customer.query.get(request.form['c_id'])
    if customer:
        customer.name = request.form['name']
        customer.mail = request.form['mail']
        customer.address = request.form['address']
        db.session.commit()
    return redirect(url_for('admin.admin'))


@admin.route('/delete-customer', methods=['POST'])
@login_required
def delete_customer():
    customer = Customer.query.get(request.form['c_id'])
    if customer:
        db.session.delete(customer)
        db.session.commit()
    return redirect(url_for('admin.admin'))

# =========================
# STAFF MANAGEMENT
# =========================

@admin.route('/create-staff', methods=['POST'])
@login_required
def create_staff():
    staff = STAFF(
        username=request.form['username'],
        email=request.form['email'],
        password=request.form['password'],  # already hashed elsewhere
        isadmin=request.form['isadmin'],
        isapproved=request.form['isapproved']
    )
    db.session.add(staff)
    db.session.commit()
    return redirect(url_for('admin.admin'))


@admin.route('/update-staff', methods=['POST'])
@login_required
def update_staff():
    staff = STAFF.query.get(request.form['s_id'])
    if staff:
        staff.username = request.form['name']
        staff.email = request.form['mail']
        staff.isadmin = request.form['isadmin']
        staff.isapproved = request.form['isapproved']
        db.session.commit()
    return redirect(url_for('admin.admin'))


@admin.route('/delete-staff', methods=['POST'])
@login_required
def delete_staff():
    staff = STAFF.query.get(request.form['s_id'])
    if staff:
        db.session.delete(staff)
        db.session.commit()
    return redirect(url_for('admin.admin'))

# =========================
# TRANSACTIONS
# =========================

@admin.route('/add-transaction', methods=['POST'])
@login_required
def add_trans():
    trans = Trans(
        c_id=request.form['c_id'],
        s_id=request.form['s_id'],
        amount=request.form['amount'],
        t_date=datetime.date.today(),
        t_time=datetime.datetime.now().time()
    )
    db.session.add(trans)
    db.session.commit()
    return redirect(url_for('admin.admin'))


@admin.route('/update-transaction', methods=['POST'])
@login_required
def update_tran():
    trans = Trans.query.get(request.form['t_id'])
    if trans:
        trans.s_id = request.form['s_id']
        trans.c_id = request.form['c_id']
        trans.amount = request.form['amount']
        trans.t_date = datetime.date.today()
        trans.t_time = datetime.datetime.now().time()
        db.session.commit()
    return redirect(url_for('admin.admin'))


@admin.route('/delete-transaction', methods=['POST'])
@login_required
def delete_tran():
    trans = Trans.query.get(request.form['t_id'])
    if trans:
        db.session.delete(trans)
        db.session.commit()
    return redirect(url_for('admin.admin'))
