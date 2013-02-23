define(['baseViewModel'], function( BaseViewModel ) {
    module('BaseViewModel Tests');

    test('BaseViewModel should convert the properties of the first argument to observables on viewModel', 4, function(){
	var model = {id: 2, list: [1, 2, 3]};
	var viewModel = new BaseViewModel(model);

	equal(typeof viewModel.id, 'function');
	equal(viewModel.id(), 2);
	equal(typeof viewModel.list.push, 'function', 'viewModel.list should have array functions');
	deepEqual(viewModel.list(), [1, 2, 3]);
    });
});