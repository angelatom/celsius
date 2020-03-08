var formElm = document.getElementById('form');
var chipInstance;

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.chips');
    var instances = M.Chips.init(elems);
    chipInstance = M.Chips.getInstance($(".chips"));
});

$("#form").submit( function(eventObj) {
    for (var i = 0; i < chipInstance.chipsData.length; i++) {
        $("<input />").attr("type", "hidden")
            .attr("name", "tags")
            .attr("value", chipInstance.chipsData[i].tag)
            .appendTo(this);
    }
    return true;
});

var checkMatching = function() {
    var checkpass = document.getElementById('check_password');
    if (checkpass.value != document.getElementById('password').value) {
        checkpass.classList = ['invalid'];
        return false;
    } else {
        checkpass.classList = ['valid'];
        return true;
    }
}

formElm.addEventListener('submit', function(e) {
    if (!checkMatching()) {
        e.preventDefault();
    }
});

document.addEventListener('DOMContentLoaded', function() {
   var elems = document.querySelectorAll('.tooltipped');
   var instances = M.Tooltip.init(elems);
 });
