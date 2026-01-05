
{username:password}
for Admin {anant:iamadmin}
for Staff {staff:staff}
for User {john:user}
(Use above username and passowrd for testing differebt roles and their interfaces)


Admin(username:anant) {email: anantweek3.dsoc@yahoo.com,password:iamadmin2024}. Use this to check otp verification.
(please use above email for testing password reset email)

download postgreSQL. open folder and activate virtual environment and select python interpreter.
open terminal and install flask,flask-login,flask-sqlalchemy,flask-mail,bcrypt and psycopg2 using pip. open psql and create database "week3_db"(using "create database week3_db;").
open init_db.py, app.py,admin.py,user.py,model.py and staff.py and change required fields like port,password etc accordingly. 
run init_db.py which creates required tables in database week3_db. 
run app.py and open localhost in browser to open the 

_**TASKS:**_

1. CRUD OPERATIONS ON staff model.
2. CRUD OPERATIONS ON transaction model.
3. CRUD OPERATIONS ON customer model.
4. Operations like adding staff, updating, deleting are for admin only.
5. Only admin can approve Staff and User to become Admin and staff respectively.
6. Staffs and USers can request for approval
7. Proper relationships between transactions , staff and customers model.
8. Password is hashed and stored in database so, password is secured and ensured secured password handling.

_**BONUS TASKS**_

1. Password reset: can send password reset mail (on registerd mail) if they forget their password.
2. Logging and Monitoring: login logout activites are monitored.
3. Advanced ROle Management: Roles are divided : Admin, STaff, User. And have interfaces accordingly.
   Admin can implement all CRUD operation on customer,staff and transaction model, can approve staffs and users for role increase, can see login activity of admins,staffs and users.
   Staff can also implement crud operations but in limited way. It can send request admin for becoming an admin.
   User cant do anything , just request admin for becoming a staff.

   If Admin approve their request their interface will change accordingly.
   
   
