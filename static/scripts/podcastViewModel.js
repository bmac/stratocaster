define(['baseViewModel', 'knockout-2.2.1', 'vent'], function(BaseViewModel, ko, vent) {
    var url = '/resources/podcast/:podcast_id/episode/:episode_id/listened_to/';
    var podcastViewModel = BaseViewModel.extend({
	defaults: {
	    filtered: true
	},
	init: function(podcast) {
	    var self = this;
	    podcast.episode_set.forEach(function(episode) {
		episode.listened_to = ko.observable(episode.listened_to);
		episode.listened_to.subscribe(function(new_value) {
		    var update_url = url.replace(':podcast_id', podcast.id)
		                        .replace(':episode_id', episode.id);

		    $.post(update_url, {listened_to: new_value});
		});
	    });
	    self._super(podcast);

	    self.episodes = ko.computed(function() {
		if (self.filtered()) {
		    return self.episode_set().filter(function(episode) {
			return episode.listened_to() === false;
		    });
		}
		return self.episode_set();
	    });
	},
	playPodcast: function(episode) {
	    vent.trigger('playAudio', episode.link);
	}
    });

    return podcastViewModel;
});