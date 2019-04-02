$(document).ready(function () {
    $(document).on('click', ".answer-edit.button", function () {
        event.preventDefault();
        let button = $(this);
        let answerId = button.attr('data-answer-id');
        let modalWrapper = $('.modal-wrapper');


        $.ajax({
            type: "GET",
            url: '/actions/edit-answer/' + answerId,
            data: {},
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                modalWrapper.append(response);
                let answerEditModal = $('.update-answer');
                answerEditModal.modal({onHidden:function () {
                        answerEditModal.remove()
                    }}).modal('show')
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        })
    });
});
