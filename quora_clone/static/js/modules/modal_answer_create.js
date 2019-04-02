$(document).ready(function () {
    $(document).on('click', ".answer.button", function () {
        event.preventDefault();
        let button = $(this);
        let questionId = button.attr('data-question-id');
        let modalWrapper = $('.modal-wrapper');


        $.ajax({
            type: "GET",
            url: '/actions/create-answer/',
            data: {question_id: questionId},
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                modalWrapper.append(response);
                let answerCreateModal = $('.create-answer.modal');
                answerCreateModal.modal({onHidden:function () {
                        answerCreateModal.remove()
                    }}).modal('show')
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        })
    });
});
