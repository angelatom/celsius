var last;

document.addEventListener('click', function(e) {
    if (e.target.hasAttribute('data-buddyID')) {
        $.ajax({
            url: 'addbuddyajax',
            method: 'POST',
            data: {buddyID: e.target.getAttribute('data-buddyID')}
        }).done(function (data) {
            console.log(data);
        });
    }
});