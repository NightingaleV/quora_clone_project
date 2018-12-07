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
$('.button-bookmark').on('click',
    function () {
        event.preventDefault();
        var button = $(this);
        var answerId = button.attr('data-answer-id');
        $.ajax({
            type:'POST',
            url: '/topics/bookmark/answer/',
            data: {answer_id: answerId},
            success: function (response) {
                console.log('Success to contact the server');
                console.log(response);
                if (response === 'saved'){
                    console.log('answer saved');
                    button.removeClass('basic');
                    button.addClass('grey');
                }
                else{
                    console.log('answer unsaved');
                    button.removeClass('grey');
                    button.addClass('basic');
                }
            },
            error: function (response) {
                console.log('Failure, request not reach the database');
            }
        })
    });
$('.follow-question-button').on('click',
    function () {
        event.preventDefault();
        let button = $(this);
        let questionId = button.attr('data-question-id');
        let buttonIcon = button.find('.icon');
        let buttonText = button.find('.follow-question-text');
        let followCounter = button.closest('.follow-question-wrapper').find('.follow-question-counter');
        let numFollowers = parseInt(followCounter.text());
        $.ajax({
            type:'POST',
            url: '/topics/follow/question/',
            data: {question_id: questionId},
            success: function (response) {
                console.log('Success to contact the server');
                console.log(response);
                if (response === 'follow'){
                    console.log('follow question');
                    // Counter
                    numFollowers += 1;
                    followCounter.text(numFollowers);

                    //Button
                    buttonText.text('Saved for later');
                    button.removeClass('basic');
                    button.addClass('grey');

                    // Icon control
                    buttonIcon.removeClass('red');
                }
                else{
                    console.log('unfollow question');

                    // Counter
                    numFollowers -= 1;
                    followCounter.text(numFollowers);

                    // Button
                    buttonText.text('Save for later');
                    button.removeClass('grey');
                    button.addClass('basic');

                    // Icon control
                    buttonIcon.addClass('red');
                }
            },
            error: function (response) {
                console.log('Failure, request not reach the database');
            }
        })
    });
$('.button-subscribe').on('click',
    function () {
        event.preventDefault();
        var topicId = $(this).attr('data-topic-id');
        var subsCounter = $(this).closest('.tab-topic').find('.subscribers-counter');
        var subButtonText = $(this).find('.subscribe-text');
        var numSubs = parseInt(subsCounter.text());
        // console.log(topicId);
        // console.log(subsCounter);
        // console.log(numSubs);
        $.ajax({
            type: "POST",
            url: '/topics/subscribe/',
            data: {topic_id: topicId},
            success: function (response) {
                // console.log('Success to contact the server');
                // console.log(response);
                if (response === 'subscribed'){
                    numSubs += 1;
                    subsCounter.text(numSubs);
                    subButtonText.text('Unsubscribe')
                }
                else{
                    numSubs -= 1;
                    subsCounter.text(numSubs);
                    subButtonText.text('Subscribe')
                }
            },
            error: function (response) {
                // console.log('Failure, request not reach the database');
            },
        })
    });
$('.button-upvote').on('click',
    function () {
        event.preventDefault();
        var button = $(this);
        var answerId = button.attr('data-answer-id');
        var upvoteCounter = button.closest('.upvote-wrapper').find('.upvote-counter');
        var buttonText = button.find('.upvote-text');
        var numUpvotes = parseInt(upvoteCounter.text());
        var buttonIcon = button.find('.icon');
        $.ajax({
            type: "POST",
            url: '/topics/upvote/',
            data: {answer_id: answerId},
            success: function (response) {
                console.log('Success to contact the server');
                console.log(response);
                if (response === 'upvoted'){
                    numUpvotes += 1;
                    upvoteCounter.text(numUpvotes);
                    buttonText.text('Upvoted');
                    // Button control
                    button.removeClass('basic');
                    button.addClass('red');
                    // Icon control
                    buttonIcon.removeClass('red');
                }
                else {
                    numUpvotes -= 1;
                    upvoteCounter.text(numUpvotes);
                    buttonText.text('Upvote');
                    // Button control
                    button.removeClass('red');
                    button.addClass('basic');
                    // Icon control
                    buttonIcon.addClass('red');
                }
            },
            error: function (response) {
                console.log('Failure, request not reach the database');
            },
        })
    });
$('.ui.accordion')
    .accordion({
        selector: {
            accordion: '.answer-accordion',
            title: '.title',
            trigger: '.answer-collapse',
            content: '.content',
        },
        debug: true,
        duration:1,
        onOpen: function () {
            console.log($(this));
            var answer = $(this).closest('.answer');
            answer.find('.answer-collapse').hide();
            answer.find('.title').hide();
        },
    });

// Sticky sidebar menu
$('.ui.sticky')
  .sticky()
;