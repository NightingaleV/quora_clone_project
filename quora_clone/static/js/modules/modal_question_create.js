$(document).ready(function () {
    let requestUrl = '/actions/create-question/';

    // OPEN EDIT MODAL
    $(document).on('click', ".create-question.button", function () {
        event.preventDefault();
        let button = $(this);
        let modalWrapper = $('.modal-wrapper');

        // LOAD MODAL FROM HTTP request
        $.ajax({
            type: "GET",
            url: requestUrl,
            data: {},
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                modalWrapper.append(response);
                let questionCreateModal = $('.create-question.modal');
                questionCreateModal.modal({
                    onHidden: function () {
                        questionCreateModal.remove()
                    }
                }).modal('show');
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        })
    });
    // Submit New QUESTION
    $(document).on('click', ".create-answer .submit.button", function () {
        event.preventDefault();
        let button = $(this);
        let modal = $('.create-question.modal');
        let form = $('.create-question .form');
        let data = form.serialize();
        console.log(data);
        $.ajax({
            type: "POST",
            url: requestUrl,
            data: data,
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                modal.modal('hide');
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        });
    });
});