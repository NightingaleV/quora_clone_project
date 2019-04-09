$(document).ready(function () {
    $(document).on('click', ".upvote-wrapper > .action.button", function () {
        event.preventDefault();
        let button = $(this);
        let objectId =button.attr('data-answer-id');
        let objectCounterText = button.closest('.upvote-wrapper').find('.counter .text');
        let objectCounterIcon = button.closest('.upvote-wrapper').find('.counter .icon');
        let buttonIcon = button.find('.icon');
        let buttonText = button.find('.text');
        let objectCounterNum = parseInt(objectCounterText.text());


        $.ajax({
            type: "POST",
            url: '/actions/upvote-answer/',
            data: {
                answer_id: objectId,
            },
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                if (response['status'] === 'upvoteSaved') {
                    // From Upvote to Downvote
                    objectCounterNum += 1;
                    objectCounterText.text(objectCounterNum);
                    objectCounterIcon.removeClass('grey');
                    objectCounterIcon.addClass('red');
                    buttonText.text('Downvote');

                    button.removeClass('upvote');
                    button.addClass('downvote');

                    buttonIcon.removeClass('arrow up red');
                    buttonIcon.addClass('arrow down');

                } else if (response['status'] === 'upvoteDeleted') {
                    // From downvote to upvote
                    objectCounterNum -= 1;
                    objectCounterText.text(objectCounterNum);
                    objectCounterIcon.removeClass('red');
                    objectCounterIcon.addClass('grey');
                    buttonText.text('Upvote');

                    button.removeClass('downvote');
                    button.addClass('upvote');

                    buttonIcon.removeClass('arrow down');
                    buttonIcon.addClass('arrow up red');
                } else {
                    console.log('we Fail')
                }
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        })
    });
});