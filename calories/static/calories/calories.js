function load_entries(sort_by, token, page) {
    $.ajax({
        url: `/load_entries`,
        type: 'GET',
        data: {
            "sort_by": sort_by,
            "page": page,
        },
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
                div_entries.empty();

                // Loop through the data and create divs for each item
                for (var i = 0; i < data['entries'].length; i++) {
                    var item = data['entries'][i];

                    // Create a div element for the item
                    var div = $('<div>').addClass('entry_item');

                    // Create and append the content to the div
                    var title = $('<h4>').text(item.name);
                    var cal = $('<b>').text(item.number + " cal");
                    var time = $('<p>').text(item.timestamp);

                    var icons_div = $('<div>').css({ "flex": "1", "position": "relative" })
                    var remove_icon = $('<i>').text('delete_sweep').addClass("material-icons black-text remove_icon")

                    icons_div.append(remove_icon)
                    div.append(title, cal, time, icons_div);

                    div_entries.append(div);
                }

                const pagination = data['pagination']
                var page_info = $('<ul>').addClass('pagination');

                if (pagination.has_previous) {
                    link = $('<a>').addClass("page-link").attr('href', "#").append($('<i>').text('chevron_left').addClass('material-icons')).click(function () {
                        load_entries("default", token, pagination.current_page - 1)
                    })
                    var listItem = $('<li>').addClass('page-item').append(link);

                    page_info.append(listItem);
                }

                pagination.paginator.page_range.forEach(function (page) {
                    var link;
                    if (page === pagination.current_page) {
                        link = $('<a>').addClass('page-link').text(page).attr('href', '#').click(function () {
                            load_entries("default", token, page);
                        });
                        var listItem = $('<li>').addClass('page-item active').append(link);
                    } else {
                        link = $('<a>').addClass('page-link').text(page).attr('href', '#').click(function () {
                            load_entries("default", token, page);
                        });
                        var listItem = $('<li>').addClass('page-item').append(link);

                    }
                    page_info.append(listItem);
                });

                if (pagination.has_next) {
                    var nextLink = $('<a>').addClass('page-link').attr('href', '#').append($('<i>').text('chevron_right').addClass('material-icons')).click(function () {
                        load_entries("default", token, pagination.current_page + 1);
                    });

                    var nextListItem = $('<li>').addClass('page-item').append(nextLink);

                    page_info.append(nextListItem);
                }
                $('#div_entries').append(page_info);

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
    load_entries("default", token, 1);


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