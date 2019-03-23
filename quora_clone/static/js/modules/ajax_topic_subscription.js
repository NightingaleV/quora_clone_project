// Show Knowledge + interest modals after subscribing
$(document).on('click', ".subscription > .button", function () {
    event.preventDefault();
    var buttonSubscribe = $(this);
    var topicId = $(this).attr('data-topic-id');
    var subsCounter = $(this).closest('.topic').find('.subs-counter');
    var subButtonIcon = $(this).find('.icon');
    var subButtonText = $(this).find('.text');
    var numSubs = parseInt(subsCounter.text());

    $.ajax({
        type: "POST",
        url: '/topics/',
        data: {topic_id: topicId},
        success: function (response) {
            // console.log('Success to contact the server');
            console.log(response);
            if (response['status'] === 'subscribed') {
                numSubs += 1;
                subsCounter.text(numSubs);
                subButtonText.text('Unsubscribe');

                buttonSubscribe.removeClass('subscribe red');
                buttonSubscribe.addClass('unsubscribe');

                subButtonIcon.removeClass('plus');
                subButtonIcon.addClass('minus');
                $('.interest.modal .rating').attr('data-topic-id', topicId);
                $('.knowledge.modal .rating').attr('data-topic-id', topicId);
                $('.interest.modal').modal('show');


            } else if (response['status'] === 'unsubscribed') {
                numSubs -= 1;
                subsCounter.text(numSubs);
                buttonSubscribe.removeClass('unsubscribe');

                subButtonText.text('Subscribe');
                buttonSubscribe.addClass('subscribe red');

                subButtonIcon.removeClass('minus');
                subButtonIcon.addClass('plus');
            } else {
                console.log('we Fail')
            }
        },
        error: function (response) {
            //console.log('Failure, request not reach the database');
        },
    })
});

// MODALS
$(document).ready(function () {
    $('.second.modal')
        .modal('attach events', '.first .icon')
    ;
    $('.second .rating').click(function () {
        $('.second.modal').modal('hide');
    });
});

$(document).ready(function () {
    // All your normal JS code goes in here
    $(".rating").rating();
    $('.rating').click(function () {
        console.log($(this).rating('get rating'))
    });
});

$('.modal.interest .rating').click(function () {
    let interestRating = $(this).rating('get rating');
    let topicId = $(this).attr('data-topic-id');
    console.log(interestRating);
    console.log(topicId);
    $.ajax({
        type: "POST",
        url: '/topics/',
        data: {
            interest_rating: interestRating, topic_id: topicId
        },
        success: function (response) {
            // console.log('Success to contact the server');
        },
        error: function (response) {
            // console.log('Failure, request not reach the database');
        },
    })
});


// Show Knowledge + interest modals after subscribing
// $(document).on('click', ".modal.interest .rating", function () {
//     let interestRating = $(this).rating('get rating');
//     let topicId = $(this).attr('data-topic-id');
//     $.ajax({
//         type: "POST",
//         url: '/topics/',
//         data: {
//             interest_rating: interestRating, topic_id: topicId
//         },
//         success: function (response) {
//             // console.log('Success to contact the server');
//         },
//         error: function (response) {
//             // console.log('Failure, request not reach the database');
//         },
//     })
// });
