define(['baseViewModel', 'knockout-2.2.1', 'vent'], function(BaseViewModel, ko, vent) {
    var AddPodcastViewModel = BaseViewModel.extend({
	el: '#add-podcast',
	defaults: {
	    link: '',
	    error: ''
	},
	init: function(observables) {
	    var self = this;
	    self._super(observables);

	    self.canCreate = ko.computed(function() {
		return !!self.link().length;
	    });
	},
	createPodcast: function() {
	    var self = this;
	    $.ajax({
		method: 'PUT',
		url: 'resources/podcast/',
		data: {
		    link: self.link().trim()
		}
	    }).done(function() {
		vent.trigger('podcastAdded');
	    }).fail(function(jqXhr) {
		self.error(jqXhr.statusText);
	    });
	}
    });

    return AddPodcastViewModel;
});