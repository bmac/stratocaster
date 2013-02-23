define(['jquery', 'baseViewModel', 'vent'], function($, BaseViewModel, vent) {
    var AudioViewModel = BaseViewModel.extend({
	el: '#audio-controls',
	defaults: {
	    audioUrl: ''
	},
	init: function(options) {
	    this._super(options);
	    this.audio = $(this.el).find('audio')[0];
	    vent.on('playAudio', this._playAudio.bind(this));
	},
	_playAudio: function(event, newAudioUrl) {
	    this.audioUrl(newAudioUrl);
	    this.audio.play();
	}
    });
    return AudioViewModel;
});