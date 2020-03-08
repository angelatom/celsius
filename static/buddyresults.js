document.addEventListener('click', function(e) {
    if (e.target.hasAttribute('data-buddyID')) {
        $.ajax({
            url: 'addbuddyajax',
            method: 'POST',
            data: {buddyID: e.target.getAttribute('data-buddyID')}
        }).done(function (data) {
            if (data.success) {
                e.target.innerText = "SENT";
                e.target.classList.add('disabled');
            }
        });
    }
});