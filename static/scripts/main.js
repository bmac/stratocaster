require.config({
    baseUrl: '/scripts/'
});
$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = $.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
require(['jquery', 'knockout-2.2.1', 'podcastViewModel'], function($, ko, PodcastViewModel) {
    $.getJSON('/resources/podcast/6/').done(function(podcast) {
	window.podcast = podcast;
	window.podcastViewModel = new PodcastViewModel(podcast);

	ko.applyBindings(podcastViewModel, $('.podcast')[0]);
    });

});
