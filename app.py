import os
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request, session, url_for, redirect, flash
from util import database

app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio = SocketIO(app)

@app.route('/')
def root():
    return render_template("base.html")
    # return "Hello world!"

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if 'userID' in session:
        return redirect(url_for("home"))
    if request.method == 'GET':
        return render_template("login.html")
    else:
        if 'username' not in request.form or 'password' not in request.form:
            flash('Please supply both a username and a password.')
            return render_template('login.html')
        userID = database.authenticate(request.form['username'], request.form['password'])
        if userID != None:
            session['userID'] = userID
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return render_template("login.html")

@app.route("/register", methods = ['POST', 'GET'])
def reg():
    if 'userID' in session:
        return redirect(url_for("home"))
    if request.method == 'GET':
        return render_template("register.html")
    else:
        for i in ['username', 'password', 'displayname']:
            if i not in request.form:
                flash('One or more fields have not been completed.')
                return redirect('/register')
        if database.registerUser(request.form['displayname'], request.form['username'], request.form['password']):
            return redirect(url_for('home'))
        else:
            flash('Username already exists!')
            return redirect('/register')

@app.route('/test')
def test():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
