QUnit.config.autostart = false;
require.config({
    baseUrl: '../scripts/'
});
require([ './tests/testBaseViewModel.js' ], function() {
    QUnit.start();
});