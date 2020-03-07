import os
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request, session, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio = SocketIO(app)

@app.route('/')
def root():
    return render_template("base.html")
    # return "Hello world!"

@app.route("/login")
def login():
    if 'username' in session:
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/register")
def reg():
    if 'username' in session:
        return redirect(url_for("home"))
    return render_template("register.html")

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
