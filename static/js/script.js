require.config({
    paths: {
        'underscore': 'libs/underscore-1.3.2.amd',
        'backbone': 'libs/backbone-0.9.2.amd',
	'podcast': 'app/podcast'
    }
  });
require(['jquery', 'underscore', 'backbone', 'podcast'], function($, _, Backbone, podcast) {
    var podcasts = new podcast.Podcasts();

    podcasts.fetch({
	success: function() {
	    console.log('podcast', podcast);
	},
	error: function() {
	    console.log('podcast', podcast);
	}
    });

    window.podcasts = podcasts;
});
