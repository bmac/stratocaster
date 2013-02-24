define(['baseViewModel', 'knockout-2.2.1', 'episodeViewModel', 'vent'], function(BaseViewModel, ko, EpisodeViewModel, vent) {

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
	    podcast.episode_set = podcast.episode_set.map(function(episode) {
		return new EpisodeViewModel(episode);
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
	    vent.trigger('playAudio', episode.link());
	}
    });

    return podcastViewModel;
});