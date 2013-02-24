define(['baseViewModel', 'knockout-2.2.1', 'podcastViewModel'], function(BaseViewModel, ko, PodcastViewModel) {
    var PodcastManager = BaseViewModel.extend({
	el: '#podcast-list',
	defaults: {
	    podcasts: []
	},
	init: function() {
	    var self = this;
	    self._super();
	    self.applyBindings();
	    $.getJSON('/resources/podcast/').done(function(podcasts) {
		var viewModels = podcasts.map(function(podcast) {
		    return new PodcastViewModel(podcast);
		});
    		self.podcasts(viewModels);
	    });
	}
    });
    return PodcastManager;
});