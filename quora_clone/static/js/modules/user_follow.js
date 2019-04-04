$(document).ready(function () {
    $(document).on('click', "button.follow-user", function () {
        event.preventDefault();
        let button = $(this);
        let objectId = button.attr('data-user-id');
        let buttonIcon = button.find('.icon');
        let buttonText = button.find('.text');

        $.ajax({
            type: "POST",
            url: '/users/follow/',
            data: {
                following_id: objectId,
            },
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                if (response['status'] === 'followingCreated') {
                    buttonText.text('Following');
                    button.removeClass('basic');


                } else if (response['status'] === 'followingDeleted') {
                    buttonText.text('Follow');
                    button.addClass('basic');
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