// $(document).ready(function () {
//     $(document).on('click', ".answer.button", function () {
//         event.preventDefault();
//         let button = $(this);
//         let questionId = button.attr('data-question-id');
//         let modalWrapper = $('.modal-wrapper');
//
//
//         $.ajax({
//             type: "GET",
//             url: '/actions/create-answer/',
//             data: {question_id: questionId},
//             success: function (response) {
//                 // console.log('Success to contact the server');
//                 console.log(response);
//                 modalWrapper.append(response);
//                 let answerCreateModal = $('.create-answer.modal');
//                 answerCreateModal.modal({onHidden:function () {
//                         answerCreateModal.remove()
//                     }}).modal('show')
//             },
//             error: function (response) {
//                 //console.log('Failure, request not reach the database');
//             },
//         })
//     });
// });

$(document).ready(function () {
    let requestUrl = '/actions/create-answer/';
    // OPEN EDIT MODAL
    $(document).on('click', ".answer.button", function () {
        event.preventDefault();
        let button = $(this);
        let questionId = button.attr('data-question-id');
        let modalWrapper = $('.modal-wrapper');

        // LOAD MODAL FROM HTTP request
        $.ajax({
            type: "GET",
            url: requestUrl,
            data: {question_id: questionId},
            success: function (response) {
                // console.log('Success to contact the server');
                console.log(response);
                modalWrapper.append(response);
                let answerCreateModal = $('.create-answer.modal');
                answerCreateModal.modal({
                    onHidden: function () {
                        answerCreateModal.remove()
                    }
                }).modal('show');
            },
            error: function (response) {
                //console.log('Failure, request not reach the database');
            },
        })
    });
    // Submit New ANSWER
    $(document).on('click', ".create-answer .submit.button", function () {
        event.preventDefault();
        let button = $(this);
        let modal = $('.create-answer.modal');
        let form = $('.create-answer .form');
        let questionId = $('.create-answer.modal .question.text').attr('data-question-id');
        let data = form.serialize() + '&question=' + questionId;

        $.ajax({
            type: "POST",
            url: requestUrl,
            data: data,
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
});
