$('.ui.accordion')
    .accordion({
        selector: {
            accordion: '.answer .accordion',
            title: '.preview',
            trigger: '.preview',
            content: '.content',
        },
        debug: true,
        duration: 1,
        onOpen: function () {
            console.log($(this));
            var answer = $(this).closest('.answer');
            //answer.find('.answer-collapse').hide();
            answer.find('.preview').hide();
        },
    });

// SIDEBAR MENU
$('.side.menu')
    .sticky({
        context: '.feed-content',
        offset: 95,
    })
;