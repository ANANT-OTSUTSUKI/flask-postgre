from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from model import db, Customer, Trans, REP, STAFF
import datetime

staff = Blueprint('staff', __name__, template_folder='templates')

# =========================
# CUSTOMER MANAGEMENT
# =========================

@staff.route('/create-customer', methods=['POST'])
@login_required
def create_customer():
    customer = Customer(
        name=request.form['name'],
        mail=request.form['mail'],
        address=request.form['address']
    )
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for('staff.staff'))


@staff.route('/update-customer', methods=['POST'])
@login_required
def update_customer():
    customer = Customer.query.get(request.form['c_id'])
    if customer:
        customer.name = request.form['name']
        customer.mail = request.form['mail']
        customer.address = request.form['address']
        db.session.commit()
    return redirect(url_for('staff.staff'))


@staff.route('/delete-customer', methods=['POST'])
@login_required
def delete_customer():
    customer = Customer.query.get(request.form['c_id'])
    if customer:
        db.session.delete(customer)
        db.session.commit()
    return redirect(url_for('staff.staff'))

# =========================
# REQUEST ADMIN APPROVAL
# =========================

@staff.route('/request-approval', methods=['POST'])
@login_required
def req_admin():
    existing = REP.query.filter_by(s_id=current_user.s_id).first()
    if existing:
        return 'APPROVAL IS ALREADY IN PROCESS'

    req = REP(
        s_id=current_user.s_id,
        username=current_user.username
    )
    db.session.add(req)
    db.session.commit()
    return 'APPROVAL REQUESTED'

# =========================
# TRANSACTIONS
# =========================

@staff.route('/add-transaction', methods=['POST'])
@login_required
def add_trans():
    trans = Trans(
        c_id=request.form['c_id'],
        s_id=current_user.s_id,
        amount=request.form['amount'],
        t_date=datetime.date.today(),
        t_time=datetime.datetime.now().time()
    )
    db.session.add(trans)
    db.session.commit()
    return redirect(url_for('staff.staff'))


@staff.route('/update-transaction', methods=['POST'])
@login_required
def update_trans():
    trans = Trans.query.get(request.form['t_id'])
    if trans:
        trans.c_id = request.form['c_id']
        trans.amount = request.form['amount']
        trans.t_date = datetime.date.today()
        trans.t_time = datetime.datetime.now().time()
        db.session.commit()
    return redirect(url_for('staff.staff'))


@staff.route('/delete-transaction', methods=['POST'])
@login_required
def delete_trans():
    trans = Trans.query.get(request.form['t_id'])
    if trans:
        db.session.delete(trans)
        db.session.commit()
    return redirect(url_for('staff.staff'))
