from flask import Flask, request, render_template, redirect, session
from models.User import User
from configuration import Configuration
from models.Employee import Employee
from functools import wraps
import hashlib
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(Configuration)

# @app.before_request
# def make_session_permanent():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(seconds=5)

def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return function(*args, **kwargs)
    return decorated_function


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User('db.sqlite3')
        if request.form['password'] != request.form['password_confirm']:
            return render_template('user/register.html', error='Passwords do not match')
        else:
            user.create(
                username=request.form['username'],
                email=request.form['email'],
                password=hashlib.md5(request.form['password'].encode()).hexdigest()
            )
            session['username'] = request.form['username']
            return redirect('/')

    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User('db.sqlite3').get_user_by_username(username)

        if user is None:
            return render_template('auth/login.html', error='User does not exist')
        else:
            password = hashlib.md5(request.form['password'].encode()).hexdigest()
            if user[3] == password:
                session['username'] = username
                return redirect('/')
            else:
                return render_template('auth/login.html', error='Incorrect password')

    return render_template('auth/login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/')
@login_required
def index():
    employee = Employee('db.sqlite3')
    employees = employee.all()

    context = {
        'employees': employees
    }
    return render_template('home/index.html', context=context)


@app.route('/create-employee', methods=['GET', 'POST'])
@login_required
def create_employee():
    if request.method == 'POST':
        employee = Employee('db.sqlite3')
        employee.create(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            department=request.form['department'],
            salary=request.form['salary']
        )
        return redirect('/')
    return render_template('employee/create.html')

@app.route('/delete', methods=['POST'])
@login_required
def delete_employee():
    employee = Employee('db.sqlite3')
    employee.delete(request.form['id'])


app.run(debug=True)
