"use strict";

// using jQuery
function getCookie(name) {
  var cookieValue = null;

  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');

    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]); // Does this cookie string begin with the name we want?

      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

$.ajaxSetup({
  beforeSend: function beforeSend(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
"use strict";

$(document).ready(function () {
  // MODAL
  function prepareRating(topicId) {
    var interestRating = $('.interest.modal .rating');
    var knowledgeRating = $('.knowledge.modal .rating'); // Set Topic

    interestRating.attr('data-topic-id', topicId);
    interestRating.attr('data-rating', 0);
    interestRating.rating('clear rating');
    knowledgeRating.attr('data-topic-id', topicId);
    knowledgeRating.attr('data-rating', 0);
    knowledgeRating.rating('clear rating');
  } // Show Knowledge + interest modals after subscribing


  $(document).on('click', ".subscription > .button", function () {
    event.preventDefault();
    var buttonSubscribe = $(this);
    var topicId = $(this).attr('data-topic-id');
    var subsCounter = $(this).closest('.topic').find('.subs-counter');
    var subButtonIcon = $(this).find('.icon');
    var subButtonText = $(this).find('.text');
    var numSubs = parseInt(subsCounter.text());
    $.ajax({
      type: "POST",
      url: '/topics/',
      data: {
        topic_id: topicId
      },
      success: function success(response) {
        // console.log('Success to contact the server');
        console.log(response);

        if (response['status'] === 'subscribed') {
          numSubs += 1;
          subsCounter.text(numSubs);
          subButtonText.text('Unsubscribe');
          buttonSubscribe.removeClass('subscribe red');
          buttonSubscribe.addClass('unsubscribe');
          subButtonIcon.removeClass('plus');
          subButtonIcon.addClass('minus');
          prepareRating(topicId);
          $('.interest.modal').modal('show');
        } else if (response['status'] === 'unsubscribed') {
          numSubs -= 1;
          subsCounter.text(numSubs);
          buttonSubscribe.removeClass('unsubscribe');
          subButtonText.text('Subscribe');
          buttonSubscribe.addClass('subscribe red');
          subButtonIcon.removeClass('minus');
          subButtonIcon.addClass('plus');
        } else {
          console.log('we Fail');
        }
      },
      error: function error(response) {//console.log('Failure, request not reach the database');
      }
    });
  });
  $('.second.modal').modal('attach events', '.first .icon');
  $('.second .rating').click(function () {
    $('.second.modal').modal('hide');
  });
});
$(document).ready(function () {
  // All your normal JS code goes in here
  $(".rating").rating(); // $('.rating').click(function () {
  //     console.log($(this).rating('get rating'))
  // });
}); // Show Knowledge + interest modals after subscribing

$(document).on('click', ".modal.interest .rating", function () {
  var topicId = $(this).attr('data-topic-id');
  console.log(topicId);
  var interestRating = $(this).rating('get rating');
  console.log(interestRating);
  $.ajax({
    type: "POST",
    url: '/topics/',
    data: {
      interest_rating: interestRating,
      topic_id: topicId
    },
    success: function success(response) {
      // console.log('Success to contact the server');
      console.log(response);

      if (response['status'] === 'rating_saved') {} else {
        console.log('we Fail');
      }
    },
    error: function error(response) {//console.log('Failure, request not reach the database');
    }
  });
}); // Show Knowledge + interest modals after subscribing

$(document).on('click', ".modal.knowledge .rating", function () {
  var topicId = $(this).attr('data-topic-id');
  console.log(topicId);
  var knowledgeRating = $(this).rating('get rating');
  console.log(knowledgeRating);
  $.ajax({
    type: "POST",
    url: '/topics/',
    data: {
      knowledge_rating: knowledgeRating,
      topic_id: topicId
    },
    success: function success(response) {
      // console.log('Success to contact the server');
      console.log(response);

      if (response['status'] === 'rating_saved') {} else {
        console.log('we Fail');
      }
    },
    error: function error(response) {//console.log('Failure, request not reach the database');
    }
  });
});
"use strict";

$('.ui.accordion').accordion({
  selector: {
    accordion: '.answer .accordion',
    title: '.preview',
    trigger: '.preview',
    content: '.content'
  },
  debug: true,
  duration: 1,
  onOpen: function onOpen() {
    console.log($(this));
    var answer = $(this).closest('.answer'); //answer.find('.answer-collapse').hide();

    answer.find('.preview').hide();
  }
});
"use strict";

// Semantic Message Closing Button
$('.message .close').on('click', function () {
  $(this).closest('.message').transition('fade');
});
$(document).ready(function () {
  $('.menu .item').tab({
    history: false
  });
});