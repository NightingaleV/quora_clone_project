$(document).ready(function () {
    // MODAL
    function prepareRating(topicId) {
        let interestRating = $('.interest.modal .rating');
        let knowledgeRating = $('.knowledge.modal .rating');
        // Set Topic
        interestRating.attr('data-topic-id', topicId);
        interestRating.attr('data-rating', 0);
        interestRating.rating('clear rating');
        knowledgeRating.attr('data-topic-id', topicId);
        knowledgeRating.attr('data-rating', 0);
        knowledgeRating.rating('clear rating');


    }
    // Show Knowledge + interest modals after subscribing
    $(document).on('click', ".subscription > .button", function () {
        event.preventDefault();
        let buttonSubscribe = $(this);
        let topicId = $(this).attr('data-topic-id');
        let subsCounter = $(this).closest('.topic').find('.subs-counter');
        let subButtonIcon = $(this).find('.icon');
        let subButtonText = $(this).find('.text');
        let numSubs = parseInt(subsCounter.text());


        $.ajax({
            type: "POST",
            url: '/topics/',
            data: {topic_id: topicId},
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                if (response['status'] === 'subscribed') {
                    console.log(topicId);
                    numSubs += 1;
                    subsCounter.text(numSubs);
                    subButtonText.text('Unsubscribe');

                    buttonSubscribe.removeClass('subscribe red inverted');
                    buttonSubscribe.addClass('unsubscribe basic');

                    subButtonIcon.removeClass('plus');
                    subButtonIcon.addClass('minus');
                    prepareRating(topicId);

                    $('.interest.modal').modal('show');


                } else if (response['status'] === 'unsubscribed') {
                    numSubs -= 1;
                    subsCounter.text(numSubs);
                    buttonSubscribe.removeClass('unsubscribe basic');

                    subButtonText.text('Subscribe');
                    buttonSubscribe.addClass('subscribe red inverted');

                    subButtonIcon.removeClass('minus');
                    subButtonIcon.addClass('plus');
                } else {
                    console.log('Integrity Error')
                }
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        })
    });

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
    // $('.rating').click(function () {
    //     console.log($(this).rating('get rating'))
    // });
});

// Show Knowledge + interest modals after subscribing
$(document).on('click', ".modal.interest .rating", function () {
    let topicId = $(this).attr('data-topic-id');
    console.log(topicId);
    let interestRating = $(this).rating('get rating');
    console.log(interestRating);

    $.ajax({
        type: "POST",
        url: '/topics/',
        data: {
            interest_rating: interestRating,
            topic_id: topicId
        },
        success: function (response) {
            // console.log('Success to contact the server');
            console.log(response);
            if (response['status'] === 'rating_saved') {
                $('.second.modal').modal('show');
                $('.first.modal').modal('hide');

            } else {
                console.log('we Fail')
            }
        },
        error: function (response) {
            //console.log('Failure, request not reach the database');
        },
    })

});
// Show Knowledge + interest modals after subscribing
$(document).on('click', ".modal.knowledge .rating", function () {
    let topicId = $(this).attr('data-topic-id');
    console.log(topicId);
    let knowledgeRating = $(this).rating('get rating');
    console.log(knowledgeRating);
    $.ajax({
        type: "POST",
        url: '/topics/',
        data: {
            knowledge_rating: knowledgeRating,
            topic_id: topicId
        },
        success: function (response) {
            // console.log('Success to contact the server');
            console.log(response);
            if (response['status'] === 'rating_saved') {

            } else {
                console.log('we Fail')
            }
        },
        error: function (response) {
            //console.log('Failure, request not reach the database');
        },
    })

});