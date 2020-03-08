var socket = io.connect('http://' + document.domain + location.port);
var whiteboard = document.getElementById('whiteboard')

socket.on('connect', function() {
    console.log("The bluetoos device has been connecte-uh successfullay!")
})

socket.on('message', function(msg) { 
    var chatlog = document.getElementById('chatlog');
    var newMsg = document.createElement('li');
    newMsg.innerHTML = msg; 
    chatlog.appendChild(newMsg) 
  })

var sendMessage = function() { 
    var newMsg = msgbox.value;
    socket.send(newMsg);
    msgbox.value = "";
}

msgbox.addEventListener("keydown", function(event) {
    if (event.keyCode == 13) {
      event.preventDefault();
      sendMessage();
    }
  })