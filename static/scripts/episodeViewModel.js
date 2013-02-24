define(['baseViewModel', 'knockout-2.2.1'], function(BaseViewModel, ko) {
    var url = 'episode/:episode_id/listened/';

    var EpisodeViewModel = BaseViewModel.extend({
	init: function(episode) {
	    this._super(episode);
	    this.listened.subscribe(this._updateListened.bind(this));
	},
	_updateListened: function(new_value) {
	    var update_url = this.podcast + url.replace(':episode_id', this.id);
	    $.post(update_url, {listened: new_value});
	}
    });

    return EpisodeViewModel;
});