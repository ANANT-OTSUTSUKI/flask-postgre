from flask import Flask, render_template, redirect, request, url_for, make_response
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from flask_mail import Mail, Message
import os
import bcrypt
from random import randint
import datetime
import logging

from model import db, STAFF
from admin import admin
from staff import staff
from user import user

# =========================
# APP SETUP
# =========================

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

logging.basicConfig(level=logging.DEBUG)
app.config["PROPAGATE_EXCEPTIONS"] = True

# =========================
# DATABASE CONFIG (RAILWAY)
# =========================

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# =========================
# 🚨 TEMPORARY INIT DB 🚨
# REMOVE AFTER FIRST SUCCESSFUL DEPLOY
# =========================

from init_db import init_database
init_database()

# =========================
# MAIL CONFIG
# =========================

app.config["MAIL_SERVER"] = "smtp.mail.yahoo.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

# =========================
# LOGIN MANAGER
# =========================

login_manager = LoginManager()
login_manager.login_view = "index"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return STAFF.query.get(int(user_id))

# =========================
# BLUEPRINTS
# =========================

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(staff, url_prefix="/staff")
app.register_blueprint(user, url_prefix="/user")

# =========================
# HELPERS
# =========================

def reload_script(url: str) -> str:
    return f"""
    <script>
    setTimeout(function() {{
        window.location.assign("{url}")
    }}, 1000);
    </script>
    """

# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("index.html")
    if current_user.isadmin == "1":
        return redirect(url_for("admin.admin"))
    if current_user.isapproved == "1":
        return redirect(url_for("staff.staff"))
    return redirect(url_for("user.user"))

@app.route("/auth", methods=["POST"])
def auth():
    username = request.form["username"]
    password = request.form["password"].encode()

    staff = STAFF.query.filter_by(username=username).first()

    if not staff:
        return redirect(url_for("index"))

    if bcrypt.checkpw(password, bytes.fromhex(staff.password)):
        login_user(staff)
        return redirect(url_for("index"))

    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# =========================
# OTP RESET
# =========================

@app.route("/otp-req", methods=["POST"])
def otp_req():
    username = request.form["username"]
    staff = STAFF.query.filter_by(username=username).first()

    if not staff:
        return "Invalid username" + reload_script("/")

    otp = randint(100000, 999999)

    resp = make_response(render_template("validate.html"))
    resp.set_cookie("otp", str(otp), max_age=300)
    resp.set_cookie("username", username, max_age=600)

    msg = Message(
        "OTP",
        sender=app.config["MAIL_USERNAME"],
        recipients=[staff.email]
    )
    msg.body = str(otp)
    mail.send(msg)

    return resp

@app.route("/change-password", methods=["POST"])
def change_pwd():
    pwd = request.form["password"].encode()
    username = request.cookies.get("username")

    staff = STAFF.query.filter_by(username=username).first()
    if not staff:
        return redirect(url_for("index"))

    staff.password = bcrypt.hashpw(pwd, bcrypt.gensalt()).hex()
    db.session.commit()

    return redirect(url_for("index"))
