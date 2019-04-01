$(document).ready(function () {
    $(document).on('click', "button.follow-question", function () {
        event.preventDefault();
        let button = $(this);
        let objectId = button.attr('data-question-id');
        let userId = button.attr('data-user-id');
        let objectCounterText = button.closest('.follow-question-wrapper').find('.counter .text');
        let objectCounterNum = parseInt(objectCounterText.text());
        let buttonIcon = button.find('.icon');
        let buttonText = button.find('.text');

        $.ajax({
            type: "POST",
            url: '/actions/follow-question/',
            data: {
                question_id: objectId,
                user_id: userId,
            },
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                if (response['status'] === 'questionFollowed') {
                    objectCounterNum += 1;
                    objectCounterText.text(objectCounterNum);
                    buttonText.text('Following Question');
                    buttonIcon.removeClass('blue')

                } else if (response['status'] === 'questionUnfollowed') {
                    objectCounterNum -= 1;
                    objectCounterText.text(objectCounterNum);
                    buttonText.text('Follow Question');
                    buttonIcon.addClass('blue')
                } else {
                    console.log('Failed')
                }
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        })
    });
});