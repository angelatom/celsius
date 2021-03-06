import os, html
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from flask import Flask, render_template, request, session, url_for, redirect, flash
from util import database

app = Flask(__name__)
app.secret_key = os.urandom(32)
socketio = SocketIO(app)

displayNames = {} # userID : displayNames
users = {} # request.sid : userID
rooms = {} # request.sid : channelID

@app.route('/')
def root():
    if 'userID' in session:
        return redirect('/dashboard')
    else:
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
            if i not in request.form or len(request.form[i]) == 0:
                flash('One or more fields have not been completed.')
                return redirect('/register')
        if database.registerUser(request.form['displayname'], request.form['username'], request.form['password']):
            tags = []
            if 'tags' in request.form:
                tags = request.form.getlist('tags')
            database.updateTags(database.getID(request.form['username']), tags)
            return redirect('/dashboard')
        else:
            flash('Username already exists!')
            return redirect('/register')

@app.route('/settings', methods = ['POST', 'GET'])
def settings():
    if 'userID' not in session:
        return redirect('/')
    if request.method == 'POST':
        if 'tags' in request.form:
            database.updateTags(session['userID'], request.form.getlist('tags'))
        if 'displayname' in request.form and len(request.form['displayname']) != 0:
            database.changeDisplayName(session['userID'], request.form['displayname'])
        if 'password' in request.form and len(request.form['password']) != 0:
            database.changePassword(session['userID'], request.form['password'])
        flash("Information updated")
        return render_template('settings.html')
    else:
        return render_template('settings.html')

@app.route('/logout')
def logout():
    if 'userID' in session:
        session.pop('userID')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'userID' not in session:
        return redirect('/')
    userdata = database.getUserInfo(session['userID'])
    displayname = userdata[1]
    username = userdata[2]
    tags = database.getTags(session['userID'])
    results = database.getBuddies(session['userID'])
    userdata = []
    for userID in results:
        userdata.append(database.getUserInfo(userID[0]))
    tag = []
    for userID in results:
        tag.append(database.getTags(userID[0]))
    buddyresults = []
    for counter in range(len(results)):
        adder = [userdata[counter], tag[counter]]
        buddyresults.append(adder)
    reqresults = database.getBuddyReq(session['userID'])
    requserdata = []
    for userID in reqresults:
        requserdata.append(database.getUserInfo(userID[0]))
    reqtags = []
    for userID in reqresults:
        reqtags.append(database.getTags(userID[0]))
    reqbuddyresults = []
    for counter in range(len(reqresults)):
        adder = [requserdata[counter], reqtags[counter]]
        reqbuddyresults.append(adder)
    #pending reqs
    rbud = database.getPendingInvites(session['userID'])
    ruserdata = []
    for userID in rbud:
        ruserdata.append(database.getUserInfo(userID[0]))
    rtags = []
    for userID in rbud:
        rtags.append(database.getTags(userID[0]))
    rresults = []
    for counter in range(len(rbud)):
        adder = [ruserdata[counter], rtags[counter]]
        rresults.append(adder)
    
    return render_template('dashboard.html', name = displayname, user = username, tags = tags, buddy = buddyresults, invites = reqbuddyresults, results = rresults)

@app.route('/studyspace')
def test():
    if 'userID' not in session:
        return redirect('/')
    return render_template('studyspace.html')

@app.route('/studybuddy')
def find_study_buddy():
    if 'userID' not in session:
        return redirect('/')
    return render_template('find.html')

@app.route('/findbuddy', methods=['POST', 'GET'])
def find_buddy_results():
    if 'userID' not in session:
        return redirect('/')
    results = database.matchTags(session['userID'])
    userdata = []
    for userID in results:
        userdata.append(database.getUserInfo(userID[0]))
    tags = []
    for userID in results:
        tags.append(database.getTags(userID[0]))
    buddyresults = []
    for counter in range(len(results)):
        adder = [userdata[counter], tags[counter]]
        buddyresults.append(adder)
    return render_template('buddyresults.html', results = buddyresults)

@app.route('/findstudyspace', methods=['POST', 'GET'])
def findstudyspace():
    floor = None
    location = None
    space = None
    status = None
    reservable = None
    zone = None
    if request.method == "POST":
        if 'floor' in request.form and request.form['floor'] != '':
            floor = request.form['floor']
            print(floor)
        if 'location' in request.form and request.form['location'] != '':
            location = request.form['location']
        if 'space' in request.form and request.form['space'] != '':
            space = request.form['space']
        if 'status' in request.form and request.form['status'] != '':
            status = request.form['status']
        if 'reservable' in request.form and request.form['reservable'] != '':
            reservable = request.form['reservable']
        if 'zone' in request.form and request.form['zone'] != '':
            zone = request.form['zone']
    print(request.form)
    '''
    data = libraryspaces.querySpaceInfo(floor = floor, location = location, space_title = space, status = status, reservable = reservable, zone_description=zone)
    if (floor == None and location == None and space == None and status == None and reservable == None and zone == None):
        ret = data[1:11]
    else:
        ret = data[1:10]
	
    = [{'space_title':'bob','status':'blah','location':'lib','zone':'Blue','zone_description':'bob','room_number':'1','floor':'5','capacity':'sad','reservable':'yes'}]
    '''
    ret = []
    return render_template('studyspaceresult.html', studyspot = ret)

@app.route('/studytools', methods = ['POST'])
def studytools():
    if 'userID' not in session:
        return redirect('/login')
    if request.method == 'POST':
        buddyID = -1
        try:
            buddyID = int(request.form['buddyID'])
        except:
            return redirect('/dashboard')
        if database.getUserInfo(buddyID) == None:
            return redirect('/dashboard')
        channelID = database.getChannel(session['userID'], buddyID)
        return render_template('studytools.html', channelID = channelID)
    else:
        return redirect('/dashboard')

@app.route('/tools')
def tools():
    if 'userID' not in session:
        return redirect('/login')
    results = database.getBuddies(session['userID'])
    userdata = []
    for userID in results:
        userdata.append(database.getUserInfo(userID[0]))
    tags = []
    for userID in results:
        tags.append(database.getTags(userID[0]))
    buddyresults = []
    for counter in range(len(results)):
        adder = [userdata[counter], tags[counter]]
        buddyresults.append(adder)
    return render_template('tools.html', buddy = buddyresults)

@app.route('/addbuddyajax', methods = ['POST'])
def addbuddyajax():
    # print(request.form)
    database.sendBuddyReq(session['userID'], request.form['buddyID'])
    return {'success' : True}

@app.route('/acceptbuddyajax', methods= ['POST'])
def acceptbuddyajax():
    return {'success' : database.acceptReq(request.form['buddyID'], session['userID'])}
    #flash("Accepted Study Buddy Request!")
    # return redirect('/buddyinvitations')

@app.route('/buddyinvitations')
def buddyinvitations():
    results = database.getBuddyReq(session['userID'])
    print(results)
    userdata = []
    for userID in results:
        userdata.append(database.getUserInfo(userID[0]))
    tags = []
    for userID in results:
        tags.append(database.getTags(userID[0]))
    buddyresults = []
    for counter in range(len(results)):
        adder = [userdata[counter], tags[counter]]
        buddyresults.append(adder)
    return render_template('invites.html', invites = buddyresults)

@app.route('/buddies')
def buddies():
    results = database.getBuddies(session['userID'])
    userdata = []
    for userID in results:
        userdata.append(database.getUserInfo(userID[0]))
    tags = []
    for userID in results:
        tags.append(database.getTags(userID[0]))
    buddyresults = []
    for counter in range(len(results)):
        adder = [userdata[counter], tags[counter]]
        buddyresults.append(adder)
    return render_template("buddies.html", buddy = buddyresults)

@socketio.on('message', namespace = '/studytools')
def message(msg):
    if 'userID' not in session:
        return
    if len(msg) != 0:
        database.sendMessage(rooms[request.sid], session['userID'], html.escape(msg))
        emit('message', f"<b>{displayNames[session['userID']]}</b>: {html.escape(msg)}", broadcast = True, room = rooms[request.sid])

@socketio.on('joinRoom', namespace = '/studytools')
def joinRoom(channelID):
    if 'userID' not in session:
        return
    if not database.inChannel(channelID, session['userID']):
        return
    if request.sid in rooms:
        leave_room(rooms[request.sid])
    join_room(channelID)
    rooms[request.sid] = channelID
    users[request.sid] = session['userID']
    displayNames[session['userID']] = database.getUserInfo(session['userID'])[1]
    msgs = database.getMessages(rooms[request.sid])
    for i in range(len(msgs)):
        curr = msgs[i]
        displayName = ""
        if curr[0] in displayNames:
            displayName = displayNames[curr[0]]
        else:
            displayNames[curr[0]] = database.getUserInfo(curr[0])[1]
        msgs[i] = f"<b>{displayName}</b>: {curr[1]}"
    emit('joinedRoom', msgs)


if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
