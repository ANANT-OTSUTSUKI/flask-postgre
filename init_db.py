"""
init_db.py
Run this file ONCE to:
1. Create all tables
2. (Optional) Seed initial users

Works with Railway + SQLAlchemy
"""

import bcrypt
from app import app
from model import db, STAFF, Customer, Trans, REQ, REP


def init_database():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created.")

        # =========================
        # OPTIONAL: SEED USERS
        # =========================

        if STAFF.query.count() == 0:
            print("Seeding initial users...")

            admin_pwd = bcrypt.hashpw(b"iamadmin", bcrypt.gensalt()).hex()
            user_pwd = bcrypt.hashpw(b"user", bcrypt.gensalt()).hex()
            staff_pwd = bcrypt.hashpw(b"staff", bcrypt.gensalt()).hex()

            users = [
                STAFF(
                    username="anant",
                    email="anantweek3.dsoc@yahoo.com",
                    password=admin_pwd,
                    isadmin='1',
                    isapproved='1'
                ),
                STAFF(
                    username="john",
                    email="john@gmail.com",
                    password=user_pwd,
                    isadmin='0',
                    isapproved='0'
                ),
                STAFF(
                    username="staff",
                    email="staff@gmail.com",
                    password=staff_pwd,
                    isadmin='0',
                    isapproved='1'
                ),
            ]

            db.session.add_all(users)
            db.session.commit()
            print("Users seeded.")
        else:
            print("Users already exist. Skipping seeding.")


if __name__ == "__main__":
    init_database()
