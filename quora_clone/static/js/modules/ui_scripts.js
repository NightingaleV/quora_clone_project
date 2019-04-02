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
