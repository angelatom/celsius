var protocol = (new URL(document.location)).protocol;
var socket = io.connect(protocol + '//' + document.domain + ':' + location.port + '/studytools');
var whiteboard = document.getElementById('whiteboard');
var chatBox = document.getElementById('chatBox');
var msgtosend = document.getElementById('msgtosend');

socket.on('connect', function () {
    console.log("The bluetoos device has been connecte-uh successfullay!");
    socket.emit('joinRoom', channelID);
});

socket.on('joinedRoom', function (data) {
    var chatBox = document.getElementById('chatBox');
    var newMsg = document.createElement('li');
    for (var i = data.length - 1; i >= 0; i--) {
        newMsg.classList.add('collection-item');
        newMsg.innerHTML = data[i];
        chatBox.appendChild(newMsg);
    }
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on('message', function (msg) {
    var chatBox = document.getElementById('chatBox');
    var newMsg = document.createElement('li');
    newMsg.classList.add('collection-item');
    newMsg.innerHTML = msg;
    chatBox.appendChild(newMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
});

var sendMessage = function () {
    var newMsg = msgtosend.value;
    if (!(newMsg == '')) {
        socket.emit('message', newMsg);
        msgtosend.value = "";
    }
}

msgtosend.addEventListener("keydown", function (event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        sendMessage();
    }
});

chatBox.scrollTop = chatBox.scrollHeight;