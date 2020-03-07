import os
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request, session, url_for, redirect, flash
from util import database

app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio = SocketIO(app)

@app.route('/')
def root():
    return render_template("home.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if 'userID' in session:
        return redirect('/dashboard')
    if request.method == 'GET':
        return render_template("login.html")
    else:
        if 'username' not in request.form or 'password' not in request.form:
            flash('Please supply both a username and a password.')
            return render_template('login.html')
        userID = database.authenticate(request.form['username'], request.form['password'])
        if userID != None:
            session['userID'] = userID
            return redirect('/dashboard')
        else:
            flash('Invalid username or password.')
            return render_template("login.html")

@app.route("/register", methods = ['POST', 'GET'])
def register():
    if 'userID' in session:
        return redirect('/')
    if request.method == 'GET':
        return render_template("register.html")
    else:
        for i in ['username', 'password', 'displayname']:
            if i not in request.form:
                flash('One or more fields have not been completed.')
                return redirect('/register')
        if database.registerUser(request.form['displayname'], request.form['username'], request.form['password']):
            return redirect('/dashboard')
        else:
            flash('Username already exists!')
            return redirect('/register')

@app.route('/settings')
def settings():
    # if 'userID' not in session:
    #     return redirect('/')
    # else:
        return render_template('settings.html')

@app.route('/logout')
def logout():
    if 'userID' in session:
        session.pop('userID')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
