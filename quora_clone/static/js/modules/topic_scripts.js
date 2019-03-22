$('.btn-subscribe').click(function () {
    // show first now
    $('.first.modal')
        .modal('show')
    ;
    // attach events to buttons
    $('.second.modal')
        .modal('attach events', '.first .icon')
    ;
});

$(document).ready(function () {
    // All your normal JS code goes in here
    $(".rating").rating();
    $('.rating').click(function () {
        console.log($(this).rating('get rating'))
    });
});


$('.second .rating').click(function () {
    $('.second.modal').modal('hide');
});