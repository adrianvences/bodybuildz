from flask_app import app
from flask_app.models.user_model import User 
from flask import Flask , render_template,request, redirect, request,flash,session
from flask_app import app,bcrypt


@app.route('/')
def redirect_home():
    return redirect('/bodybuildz')


@app.route('/bodybuildz')
def index():
    return render_template('index.html')


@app.route('/login/register')
def login_register():
    return render_template('login.html')

@app.route('/your_feed')
def users_dashboard():
    if not 'uid' in session:
        flash('please login first!')
        return redirect('/login/register')

    logged_in_user = User.find_by_user(session['uid'])
    return render_template('users_dashboard.html', user=logged_in_user)

@app.route('/test_home')
def test():
    return render_template('new_home.html')

#------ create route -------#
@app.route ('/register', methods=['post'])
def register ():
    print(request.form)

    if not User.validate(request.form):
        return redirect('/login/register')

        #---- this hashs our password -----#
    hash = bcrypt.generate_password_hash(request.form['password'])

    new_user = {
        'first_name' :request.form ['first_name'],
        'last_name' :request.form ['last_name'],
        'email' : request.form ['email'],
        'gym_level' : request.form ['gym_level'], 
        'password' : hash 
    }
    #--- had to turn this into create var----# 
    #--- then use session to pull uid from create---#
    create = User.create_user(new_user)

    session['uid'] = create

    return redirect('/your_feed')


#-------- route to login---------#
@app.route ('/login', methods=['POST'])
def login():

    logged_in_user = User.validate_login(request.form)

    if not logged_in_user:
        return redirect('/login/register')
    session['uid'] = logged_in_user.id
    # print(request.form)
    return redirect('/your_feed')



@app.route('/logout')
def logout ():
    session.clear()
    return redirect ('/')