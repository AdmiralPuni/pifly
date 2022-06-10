$(document).ready(function() {
    $.ajax({
        url: '/user/data',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#user-name').text(data.name);
        }
    });
});