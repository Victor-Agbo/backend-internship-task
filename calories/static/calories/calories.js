function load_entries(sort_by, token) {
    $.ajax({
        url: `/load_entries/${sort_by}`,  // Replace with the actual API endpoint URL
        type: 'GET',
        contentType: "application/json",
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Token ' + token);
        },
        success: function (data) {
            // Handle successful response
            console.log(data);

            renderData(data);

            function renderData(data) {
                var div_entries = $('#div_entries');

                // Clear the mainDiv contents before rendering
                div_entries.empty();

                // Loop through the data and create divs for each item
                for (var i = 0; i < data.length; i++) {
                    var item = data[i];

                    // Create a div element for the item
                    var div = $('<div>').addClass('entry_item');

                    // Create and append the content to the div
                    var inner_div = $('<div>').addClass('container');
                    var title = $('<h4>').text(item.name);

                    var cal = $('<b>').text(item.number + " cal");
                    var time = $('<p>').text(item.timestamp);

                    inner_div.append(title, cal, time);
                    div.append(inner_div)
                    // Append the div to the mainDiv
                    div_entries.append(div);
                }
            }

        },
        error: function (xhr, textStatus, errorThrown) {
            // Handle error response
            console.log(errorThrown);
        }
    });
}

$(document).ready(function () {
    // Handler for .ready() called.
    $(".dropdown-trigger").dropdown({ "hover": false });

    $('#set_calories_li').click(function () {
        $('#form_set_calories').fadeIn();
        $('#form-overlay').fadeIn();
    });

    $('#form-overlay').click(function () {
        $('#form_set_calories').fadeOut();
        $('#form_add_entry').fadeOut();
        $('#form-overlay').fadeOut();

    });

    $('#add_entry_button').click(function () {
        $('#form_add_entry').fadeIn();
        $('#form-overlay').fadeIn();
    });
    var token = $('#auth_token').val();
    load_entries("default", token);


    $('#new_calories_submit').click(function () {

        var data = {
            new_calories: $('#new_calories').val(),
        };
        console.log(data);

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
                $('#message').text(response['message']);
                $('#message_div').fadeIn(1000);
                $('#message_div').fadeOut(2000);

            },
            error: function (xhr, textStatus, errorThrown) {
                // Handle error response
                if (xhr.status === 401) {
                    console.log('Authentication failed. Please check your token.');
                    $('#message').text('Authentication failed...');
                    $('#message_div').fadeIn(1000);
                    $('#message').fadeOut(2000)
                } else {
                    console.log('Error:', errorThrown);
                    $('#message').text(errorThrown);
                    $('#message_div').fadeIn(1000);
                    $('#message_div').fadeOut(2000)
                }
            }
        });

        $('#form_set_calories').fadeOut();
        $('#form-overlay').fadeOut();
        return false;
    });

    $('#submit_entry').click(function () {

        var data = {
            add_meal_name: $('#add_meal_name').val(),
            add_cal_num: $('#add_cal_num').val(),
        };
        console.log(data);

        $.ajax({
            url: '/add_entry',  // Replace with the actual API endpoint URL
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + token);
            },
            success: function (response) {
                // Handle successful response
                console.log(response);
                $('#message').text(response['message']);
                $('#message_div').fadeIn(1000);
                $('#message_div').fadeOut(2000);
            },
            error: function (xhr, textStatus, errorThrown) {
                // Handle error response
                if (xhr.status === 401) {
                    console.log('Authentication failed. Please check your token.');
                    $('#message').text('Authentication failed...');
                    $('#message_div').fadeIn(1000);
                    $('#message_div').fadeOut(2000)
                } else {
                    console.log('Error:', errorThrown);
                    var errorResponse = xhr.responseJSON;
                    $('#message').text(errorResponse.message);
                    $('#message_div').fadeIn(1000);
                    $('#message_div').fadeOut(2000)
                }
            }
        });

        $('#form_add_entry').fadeOut();
        $('#form-overlay').fadeOut();
        return false;
    });
})