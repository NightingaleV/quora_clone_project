// Semantic Message Closing Button
$('.message .close')
    .on('click', function () {
        $(this)
            .closest('.message')
            .transition('fade')
        ;
    })
;

$(document).ready(function () {
    $('.menu .item').tab({history: false});
});


$(document).ready(function () {
    $('.answer.button').click(function () {
        let questionId = $(this).attr('data-question-id');
        let answerModal = $('.create-answer.modal');
        let questionIdInput = answerModal.find('.question-id-input');
        questionIdInput.val(questionId);

       answerModal.modal('show');
    });
});