from flask import Blueprint, request
from flask_login import login_required, current_user
from model import db, REQ

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/request-approval', methods=['POST'])
@login_required
def req_approval():
    # Never trust form s_id, use logged-in user
    s_id = current_user.s_id
    username = current_user.username

    existing = REQ.query.filter_by(s_id=s_id).first()
    if existing:
        return 'APPROVAL IS IN PROCESS'

    req = REQ(
        s_id=s_id,
        username=username
    )
    db.session.add(req)
    db.session.commit()

    return 'APPROVAL REQUESTED'
