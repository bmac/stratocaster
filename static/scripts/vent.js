define(['jquery'], function($) {
    var _vent = $({});

    var vent = {
	on: function() {
	    return _vent.on.apply(_vent, arguments);
	},
	off: function() {
	    return _vent.off.apply(_vent, arguments);
	},
	trigger: function() {
	    return _vent.trigger.apply(_vent, arguments);
	}
    };

    return vent;
});