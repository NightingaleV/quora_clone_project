$('.btn-subscribe').on('click', function () {
    event.preventDefault();

    var topicId = $(this).attr('data-topic-id');
    var subsCounter = $(this).closest('.tab-topic').find('.subscribers-counter');
    var subButtonText = $(this).find('.subscribe-text');
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