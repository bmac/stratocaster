define(['baseViewModel', 'knockout-2.2.1'], function(BaseViewModel, ko) {
    var url = '/resources/podcast/:podcast_id/episode/:episode_id/listened_to/';
    var podcastViewModel = BaseViewModel.extend({
	init: function(podcast) {
	    podcast.episode_set.forEach(function(episode) {
		episode.listened_to = ko.observable(episode.listened_to);
		episode.listened_to.subscribe(function(new_value) {
		    var update_url = url.replace(':podcast_id', podcast.id)
		                        .replace(':episode_id', episode.id);

		    $.post(update_url, {listened_to: new_value});
		});
	    });
	    this._super(podcast);
	}
    });

    return podcastViewModel;
});