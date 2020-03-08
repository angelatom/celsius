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