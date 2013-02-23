define(['baseViewModel', 'knockout-2.2.1', 'vent'], function(BaseViewModel, ko, vent) {
    var url = '/resources/podcast/:podcast_id/episode/:episode_id/listened/';

    var filterUnlistenedEpisodes = function(episodes) {
	return episodes.filter(function(episode) {
	    return !episode.listened();
	});
    };

    var podcastViewModel = BaseViewModel.extend({
	defaults: {
	    showNew: true
	},
	init: function(podcast) {
	    var self = this;
	    podcast.episode_set.forEach(function(episode) {
		episode.listened = ko.observable(episode.listened);
		episode.listened.subscribe(function(new_value) {
		    var update_url = url.replace(':podcast_id', podcast.id)
		                        .replace(':episode_id', episode.id);

		    $.post(update_url, {listened: new_value});
		});
	    });
	    self._super(podcast);

	    self.episodes = ko.computed(function() {
		if (self.showNew()) {
		    return filterUnlistenedEpisodes(self.episode_set());
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