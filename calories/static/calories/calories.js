$(document).ready(function () {
    $(".dropdown-trigger").dropdown({ hover: false });

    $('#set_calories_li').click(function () {
        toggleForm('#form_set_calories');
    });

    $('#form-overlay').click(function () {
        hideForms();
    });

    $('#add_entry_button').click(function () {
        toggleForm('#form_add_entry');
    });

    const token = $('#auth_token').val();
    loadEntries("default", token, 1);

    $('#crud_users_li').click(function () {
        loadUsers('default', token, 1)
    })
    $('#new_calories_submit').click(function () {
        const data = {
            new_calories: $('#new_calories').val()
        };
        sendAjaxRequest('/set_calories', 'POST', data, token);
        hideForms();
        return false;
    });

    $('#edit_entry').click(function () {
        const data = {
            edit_id: $('#edit_id').val(),
            edit_entry_user: $('#edit_entry_user'),
            edit_meal_name: $('#edit_meal_name').val(),
            edit_cal_num: $('#edit_cal_num').val()
        };
        sendAjaxRequest('/edit_entry', 'POST', data, token);
        hideForms();
        return false;
    });

    $('#edit_user').click(function () {
        const data = {
            user_id: $('#edit_user_id').val(),
            user_email: $('#edit_email').val(),
            user_per_day: $('#edit_per_day').val()
        };
        sendAjaxRequest('/edit_user', 'POST', data, token);
        hideForms();
        return false;
    });

    $('#submit_entry').click(function () {
        const data = {
            add_meal_name: $('#add_meal_name').val(),
            add_cal_num: $('#add_cal_num').val()
        };
        sendAjaxRequest('/add_entry', 'POST', data, token);
        hideForms();
        $('#add_meal_name').val("");
        $('#add_cal_num').val("");
        return false;
    });

    $('#div_entries').on('click', '.edit_icon', function () {
        const item_id = $(this).data("id");
        const item_user = $(this).data("user_id");
        const meal_name = $(this).parent().siblings('h4').text();
        const cal_num = $(this).parent().siblings('b').text().replace(' cal', '');
        $('#edit_id').val(item_id);
        $('#user_id').val(item_user);
        $('#edit_meal_name').val(meal_name);
        $('#edit_cal_num').val(cal_num);
        toggleForm('#form_edit_entry');
    });

    $('#div_entries').on('click', '.edit_user_icon', function () {
        const user_id = $(this).data("id");
        const email = $(this).parent().siblings('p').text();
        const per_day = $(this).parent().siblings('b').text().replace(' cal', '');
        $('#edit_user_id').val(user_id);
        $('#edit_email').val(email);
        $('#edit_per_day').val(per_day);
        toggleForm('#form_edit_user');
    });

    $('#div_entries').on('click', '.remove_icon', function () {
        const entryId = $(this).attr('data-id');
        deleteEntry(entryId, token);
    });

    $('#div_entries').on('click', '.remove_user_icon', function () {
        const userId = $(this).attr('data-id');
        deleteUser(userId, token);
    });
});

function toggleForm(formId) {
    $(formId).fadeIn();
    $('#form-overlay').fadeIn();
}

function hideForms() {
    $('#form_set_calories').fadeOut();
    $('#form_add_entry').fadeOut();
    $('#form_edit_entry').fadeOut();
    $('#form_edit_user').fadeOut();
    $('#form-overlay').fadeOut();
}

function sendAjaxRequest(url, method, data, token) {
    $.ajax({
        url: url,
        type: method,
        data: JSON.stringify(data),
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Token ' + token);
        },
        success: function (response) {
            handleSuccess(response);
        },
        error: function (xhr, textStatus, errorThrown) {
            handleError(xhr, errorThrown);
        }
    });
}

function handleSuccess(response) {
    $('#message').text(response['message']);
    $('#message_div').fadeIn(1000).fadeOut(2000);
    loadEntries('default', $('#auth_token').val(), $('li.active').find('a').text());
}

function handleError(xhr, errorThrown) {
    let errorMessage = '';

    if (xhr.status === 401) {
        errorMessage = 'Authentication failed. Please check your token.';
    } else {
        errorMessage = errorThrown || 'An error occurred.';
    }

    $('#message').text(errorMessage);
    $('#message_div').fadeIn(1000).fadeOut(2000);
}

function deleteUser(id, token) {
    console.log(id);
    $.ajax({
        url: `/delete_user`,
        type: 'DELETE',
        dataType: 'json',
        data: {
            "user_id": id
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Token ' + token);
        },
        success: function (data) {
            loadUsers('default', token, $('li.active').find('a').text());
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}

function deleteEntry(id, token) {
    console.log(id);
    $.ajax({
        url: `/delete_entry`,
        type: 'DELETE',
        dataType: 'json',
        data: {
            "entry_id": id
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Token ' + token);
        },
        success: function (data) {
            loadEntries('default', token, $('li.active').find('a').text());
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}

function renderData(data) {
    const divEntries = $('#div_entries');
    const token = $('#auth_token').val();
    divEntries.empty();

    for (let i = 0; i < data.entries.length; i++) {
        const item = data.entries[i];
        const div = $('<div>').addClass('entry_item');
        const title = $('<h4>').text(item.name);
        const cal = $('<b>').text(item.number + ' cal');
        const time = $('<p>').text(item.timestamp);
        const iconsDiv = $('<div>').css({ flex: '1', position: 'relative' });
        const editIcon = $('<i>')
            .text('edit')
            .addClass('material-icons black-text right edit_icon').data("id", item.id).data("user_id", item.user_id);
        const removeIcon = $('<i>')
            .text('delete_sweep')
            .addClass('material-icons black-text remove_icon')
            .attr('data-id', item.id);

        removeIcon.click(function () {
            deleteEntry($(this).attr('data-id'), token);
        });

        iconsDiv.append(editIcon, removeIcon);
        div.append(title, cal, time, iconsDiv);
        divEntries.append(div);
    }

    const pagination = data.pagination;
    const page_info = $('<ul>').addClass('pagination');

    if (pagination.has_previous) {
        const link = $('<a>')
            .addClass('page-link')
            .attr('href', '#')
            .append($('<i>').text('chevron_left').addClass('material-icons'));

        link.click(function () {
            loadEntries('default', token, pagination.current_page - 1);
        });

        const listItem = $('<li>').addClass('page-item').append(link);
        page_info.append(listItem);
    }

    pagination.paginator.page_range.forEach(function (page) {
        let link;

        if (page === pagination.current_page) {
            link = $('<a>').addClass('page-link').text(page).attr('href', '#').click(function () {
                loadEntries('default', token, page);
            });

            const listItem = $('<li>').addClass('page-item active').append(link);
            page_info.append(listItem);
        } else {
            link = $('<a>').addClass('page-link').text(page).attr('href', '#').click(function () {
                loadEntries('default', token, page);
            });

            const listItem = $('<li>').addClass('page-item').append(link);
            page_info.append(listItem);
        }
    });

    if (pagination.has_next) {
        const nextLink = $('<a>')
            .addClass('page-link')
            .attr('href', '#')
            .append($('<i>').text('chevron_right').addClass('material-icons'));

        nextLink.click(function () {
            loadEntries('default', token, pagination.current_page + 1);
        });

        const nextListItem = $('<li>').addClass('page-item').append(nextLink);
        page_info.append(nextListItem);
    }

    $('#div_entries').append(page_info);
}

function renderUsers(data) {
    const divEntries = $('#div_entries');
    const token = $('#auth_token').val();
    divEntries.empty();

    for (let i = 0; i < data.users.length; i++) {
        const user = data.users[i];
        const div = $('<div>').addClass('entry_item');
        const title = $('<h4>').text(user.username);
        const cal = $('<b>').text(user.per_day + ' cal');
        const email = $('<p>').text(user.email);
        const iconsDiv = $('<div>').css({ flex: '1', position: 'relative' });
        const editIcon = $('<i>')
            .text('edit')
            .addClass('material-icons black-text right edit_user_icon').data("id", user.id);
        const removeUser = $('<i>')
            .text('delete_sweep')
            .addClass('material-icons black-text remove_user_icon')
            .attr('data-id', user.id);

        iconsDiv.append(editIcon, removeUser);
        div.append(title, cal, email, iconsDiv);
        divEntries.append(div);
    }

    const pagination = data.pagination;
    const page_info = $('<ul>').addClass('pagination');

    if (pagination.has_previous) {
        const link = $('<a>')
            .addClass('page-link')
            .attr('href', '#')
            .append($('<i>').text('chevron_left').addClass('material-icons'));

        link.click(function () {
            loadUsers('default', token, pagination.current_page - 1);
        });

        const listItem = $('<li>').addClass('page-item').append(link);
        page_info.append(listItem);
    }

    pagination.paginator.page_range.forEach(function (page) {
        let link;

        if (page === pagination.current_page) {
            link = $('<a>').addClass('page-link').text(page).attr('href', '#').click(function () {
                loadUsers('default', token, page);
            });

            const listItem = $('<li>').addClass('page-item active').append(link);
            page_info.append(listItem);
        } else {
            link = $('<a>').addClass('page-link').text(page).attr('href', '#').click(function () {
                loadUsers('default', token, page);
            });

            const listItem = $('<li>').addClass('page-item').append(link);
            page_info.append(listItem);
        }
    });

    if (pagination.has_next) {
        const nextLink = $('<a>')
            .addClass('page-link')
            .attr('href', '#')
            .append($('<i>').text('chevron_right').addClass('material-icons'));

        nextLink.click(function () {
            loadUsers('default', token, pagination.current_page + 1);
        });

        const nextListItem = $('<li>').addClass('page-item').append(nextLink);
        page_info.append(nextListItem);
    }

    $('#div_entries').append(page_info);
}

function loadEntries(sortBy, token, page) {
    $.ajax({
        url: '/load_entries',
        type: 'GET',
        data: {
            sort_by: sortBy,
            page: page
        },
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Token ' + token);
        },
        success: function (response) {
            renderData(response);
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}

function loadUsers(sortBy, token, page) {
    $.ajax({
        url: '/load_users',
        type: 'GET',
        data: {
            "sort_by": sortBy,
            "page": page
        },
        contentType: 'application/json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Authorization', 'Token ' + token);
        },
        success: function (response) {
            renderUsers(response);
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}
