require.config({
    baseUrl: '/scripts/'
});

require(['jquery', 'knockout-2.2.1', 'baseViewModel'], function($, ko, BaseViewModel) {

    $.getJSON('/resources/podcast/6/').done(function(podcast) {
	window.podcast = podcast;
	window.podcastViewModel = new BaseViewModel(podcast);

	ko.applyBindings(podcastViewModel, $('.podcast')[0]);
    });

});
