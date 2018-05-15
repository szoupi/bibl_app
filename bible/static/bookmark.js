/**
 * Bookmark Books, Chapters, Verses and Annotations
 */

// https://evileg.com/en/post/244/
// https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html

// Getting a cookie by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Setup AJAX
$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function to_bookmarks() {
    var current = $(this);
    var type = current.data('type');
    var pk = current.data('id');
    var action = current.data('action');

    $.ajax({
        url: "/" + type + "/" + pk + "/" + action + "/",
        type: 'POST',
        data: { 'obj': pk },

        success: function (json) {
            current.find("[data-count='" + action + "']").text(json.count);
            // current.find("[data-count='" + action + "']").text(json.book_is_bookmarked);
        
        }

    });

    return false;
}

$(function () {
    $('[data-action="bookmark"]').click(to_bookmarks);
});