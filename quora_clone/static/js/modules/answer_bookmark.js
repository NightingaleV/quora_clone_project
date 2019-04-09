$(document).ready(function () {
    $(document).on('click', ".button-bookmark", function () {
        event.preventDefault();
        let button = $(this);
        let objectId = button.attr('data-answer-id');
        let objectCounter = button.closest('.topic').find('.counter');
        let buttonIcon = button.find('.icon');


        $.ajax({
            type: "POST",
            // TODO ZMENIT STRUKTURU URL AJAX REQUESTU
            url: '/actions/bookmark-answer/',
            data: {
                answer_id: objectId,
            },
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                if (response['status'] === 'bookmarkSaved') {
                    buttonIcon.addClass('red');
                } else if (response['status'] === 'bookmarkDeleted') {
                    buttonIcon.removeClass('red');
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