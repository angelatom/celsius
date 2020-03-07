import os
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request, session, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio = SocketIO(app)

@app.route('/')
def root():
    return "Hello world!"

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)