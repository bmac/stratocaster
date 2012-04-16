define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    var PodcastModel = Backbone.Model.extend({
	urlRoot: '/resources/podcast'
    });
    var Podcasts = Backbone.Collection.extend({
	model: PodcastModel,
	url: '/resources/podcast/'
    });

    return {
	PodcastModel: PodcastModel,
	Podcasts: Podcasts
    };
});
