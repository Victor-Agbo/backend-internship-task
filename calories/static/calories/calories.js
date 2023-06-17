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
        $.ajax({
            url: "/set_calories",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function (response) {
                console.log("POST request successful:", response);
                $('#message').wrapInner(response['message']);
                console.log($('#message').val());
                $('#message_div').fadeIn(1000);
                $('#message').fadeOut(2000);

            },
            error: function (xhr, status, error) {
                console.error("Error making PUT request:", error);
            }
        });
        $('#form_set_calories').fadeOut();
        $('#form-overlay').fadeOut();
        return false;
    });
})