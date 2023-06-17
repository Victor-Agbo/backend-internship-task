$(document).ready(function () {
    // Handler for .ready() called.
    $(".dropdown-trigger").dropdown({ "hover": false });

    $('#set_calories_li').click(function () {
        $('#form_set_calories').fadeIn();
        $('#form-overlay').fadeIn();
    });

    $('#form-overlay').click(function () {
        $('#form_set_calories').fadeOut();
        $('#form-overlay').fadeOut();
    });


    $('#new_calories_submit').click(function () {

        var data = {
            new_calories: $('#new_calories').val(),
        };
        console.log(data);
        var token = $('#auth_token').val();  // Replace with the actual authentication token

        $.ajax({
            url: '/set_calories',  // Replace with the actual API endpoint URL
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + token);
            },
            success: function (response) {
                // Handle successful response
                console.log(response);
                $('#message').wrapInner(response['message']);
                $('#message_div').fadeIn(1000);
                $('#message').fadeOut(2000);
            },
            error: function (xhr, textStatus, errorThrown) {
                // Handle error response
                if (xhr.status === 401) {
                    console.log('Authentication failed. Please check your token.');
                    $('#message').wrapInner('Authentication failed...');
                    $('#message_div').fadeIn(1000);
                    $('#message').fadeOut(2000)
                } else {
                    console.log('Error:', errorThrown);
                    $('#message').wrapInner(errorThrown);
                    $('#message_div').fadeIn(1000);
                    $('#message').fadeOut(2000)
                }
            }
        });

        $('#form_set_calories').fadeOut();
        $('#form-overlay').fadeOut();
        return false;
    });
})