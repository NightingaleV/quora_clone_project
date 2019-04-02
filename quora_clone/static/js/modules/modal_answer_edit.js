$(document).ready(function () {
    // OPEN EDIT MODAL
    $(document).on('click', ".edit-answer.button", function () {
        event.preventDefault();
        let button = $(this);
        let answerId = button.attr('data-answer-id');
        let modalWrapper = $('.modal-wrapper');

        // LOAD MODAL FROM HTTP request
        $.ajax({
            type: "GET",
            url: '/actions/edit-answer/' + answerId,
            data: {},
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                modalWrapper.append(response);
                let answerEditModal = $('.edit-answer.modal');
                answerEditModal.modal({
                    onHidden: function () {
                        answerEditModal.remove()
                    }
                }).modal('show');
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        })
    });
    // Submit ANSWER
    $(document).on('click', ".edit-answer .submit.button", function () {
        event.preventDefault();
        let button = $(this);
        let modal = $('.edit-answer');
        let form = $('.edit-answer .form');
        let requestUrl = form.attr('action');
        $.ajax({
            type: "POST",
            url: requestUrl,
            data: form.serialize(),
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                window.location.reload();

            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        });
    });

    // DELETE ANSWER
    $(document).on('click', ".edit-answer .delete.button", function () {
        event.preventDefault();
        let button = $('edit-answer');
        let form = $('.edit-answer .form');
        let formRequestUrl = form.attr('action');
        let urlArray = formRequestUrl.split('/');
        let requestUrl = '/actions/delete-answer/';
        let answerId = urlArray[urlArray.length - 1]
        console.log(urlArray[urlArray.length - 1]);
        $.ajax({
            type: "POST",
            url: requestUrl,
            data: {answer_id: answerId},
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                if (response['status'] === 'answerDeleted') {
                    window.location.reload();
                }
                // window.location.reload();

            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        });
    });
});
