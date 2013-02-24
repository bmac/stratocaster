define(['jquery', 'baseViewModel', 'vent'], function($, BaseViewModel, vent) {
    var AudioViewModel = BaseViewModel.extend({
	el: '#audio-controls',
	defaults: {
	    audioUrl: ''
	},
	init: function(observables) {
	    this._super(observables);
	    this.audio = $(this.el).find('audio')[0];
	    this.applyBindings();
	    vent.on('playAudio', this._playAudio.bind(this));
	},
	_playAudio: function(event, newAudioUrl) {
	    this.audioUrl(newAudioUrl);
	    this.audio.play();
	}
    });
    return AudioViewModel;
});