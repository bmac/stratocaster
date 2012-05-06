define([
  "restcast",

  // Libs
  "use!backbone"

  // Modules

  // Plugins
],

function(restcast, Backbone) {

  // Create a new module
  var Podcast = restcast.module();

  // Example extendings
  Podcast.Model = Backbone.Model.extend({
      urlRoot: '/resources/podcast/'
  });
  Podcast.Collection = Backbone.Collection.extend({
      model: Podcast.Model,
      url: '/resources/podcast/'
  });

  // This will fetch the tutorial template and render it.
  Podcast.Views.PodcastView = Backbone.View.extend({
    initialize: function(model) {
	this.model = model;
    },
    template: "app/templates/podcast.html",
    render: function(done) {
      var view = this;

      // Fetch the template, render it to the View element and call done.
      return restcast.fetchTemplate(this.template, function(tmpl) {
        view.el.innerHTML = tmpl(view);

        // If a done function is passed, call it with the element
        if (_.isFunction(done)) {
          done(view.el);
        }
      });
    },

    events: {
      "click li": "loadInPlayer"
    },

    loadInPlayer: function() {
      restcast.app.trigger("loadInPlayer", this.model.get('episode_set')[3].link );
    }
  });

  // Required, return the module for AMD compliance
  return Podcast;

});
