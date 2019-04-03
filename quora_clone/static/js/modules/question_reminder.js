$(document).ready(function () {
    $(document).on('click', "button.answer-later", function () {
        event.preventDefault();
        let button = $(this);
        let objectId = button.attr('data-question-id');
        let buttonIcon = button.find('.icon');
        let buttonText = button.find('.text');

        $.ajax({
            type: "POST",
            url: '/actions/remind-question/',
            data: {
                question_id: objectId,
            },
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                if (response['status'] === 'reminderCreated') {
                    buttonIcon.removeClass('outline')

                } else if (response['status'] === 'reminderDeleted') {
                    buttonIcon.addClass('outline')
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