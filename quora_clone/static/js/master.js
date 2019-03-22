// using jQuery
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

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
$('.btn-subscribe').on('click', function () {
    event.preventDefault();

    var topicId = $(this).attr('data-topic-id');
    var subsCounter = $(this).closest('.tab-topic').find('.subscribers-counter');
    var subButtonText = $(this).find('.subscribe-text');
    var numSubs = parseInt(subsCounter.text());

    $.ajax({
        type: "POST",
        url: '/topics/subscribe/',
        data: {topic_id: topicId},
        success: function (response) {
            // console.log('Success to contact the server');
            // console.log(response);
            if (response['status'] === 'subscribed') {
                numSubs += 1;
                subsCounter.text(numSubs);
                subButtonText.text('Unsubscribe')
            } else if (response['status'] === 'unsubscribed') {
                numSubs -= 1;
                subsCounter.text(numSubs);
                subButtonText.text('Subscribe')
            } else {
                return null
            }
        },
        error: function (response) {
            // console.log('Failure, request not reach the database');
        },
    })
});
$('.btn-subscribe').click(function () {
    // show first now
    $('.first.modal')
        .modal('show')
    ;
    // attach events to buttons
    $('.second.modal')
        .modal('attach events', '.first .icon')
    ;
});

$(document).ready(function () {
    // All your normal JS code goes in here
    $(".rating").rating();
    $('.rating').click(function () {
        console.log($(this).rating('get rating'))
    });
});


$('.second .rating').click(function () {
    $('.second.modal').modal('hide');
});
// Semantic Message Closing Button
$('.message .close')
    .on('click', function () {
        $(this)
            .closest('.message')
            .transition('fade')
        ;
    })
;

$(document).ready(function () {
    $('.menu .item').tab({history: false});
});


