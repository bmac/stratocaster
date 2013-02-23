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
require(['jquery', 'knockout-2.2.1', 'podcastViewModel', 'audioViewModel', 'addPodcastViewModel'], function($, ko, PodcastViewModel, AudioViewModel, AddPodcastViewModel) {
    var audioViewModel = new AudioViewModel();
    ko.applyBindings(audioViewModel, $(audioViewModel.el)[0]);
    var addPodcastViewModel = new AddPodcastViewModel();
    ko.applyBindings(addPodcastViewModel, $(addPodcastViewModel.el)[0]);
    var podcastManager = {
	podcasts: ko.observableArray([])
    };
    ko.applyBindings(podcastManager, $('#podcast-list')[0]);

    $.getJSON('/resources/podcast/').done(function(podcasts) {
	var viewModels = podcasts.map(function(podcast) {
	    return new PodcastViewModel(podcast);
	});
    	podcastManager.podcasts(viewModels);
    });

});
