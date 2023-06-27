from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.model.registration_model import User



@app.route('/')
def home():
    all_user = User.get_all(request.form)
    return render_template('login_registration.html', all_user = all_user)



@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    user_id = User.Create_user(request.form)

    session['user_id'] = user_id
    return redirect(f'/dashboard/{user_id}')



@app.route('/login', methods=['POST'])
def login():
    if not User.login_user(request.form):
        return redirect('/')
    email = User.GetUserByEmail(request.form)

    session['user_id'] = email.id
    return redirect(f'/dashboard')



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    newUser = User.GetUserById({'id':session['user_id']})
    return render_template('dashboard.html', newUser = newUser)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')