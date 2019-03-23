$(document).ready(function () {
    $('.second.modal')
        .modal('attach events', '.first .icon')
    ;
    $('.second .rating').click(function () {
        $('.second.modal').modal('hide');
    });
});

$(document).ready(function () {
    // All your normal JS code goes in here
    $(".rating").rating();
    $('.rating').click(function () {
        console.log($(this).rating('get rating'))
    });
});


