(function(){
	
	'use strict';

	var app = angular.module('scanner', ['ngSanitize']);

	app.directive('inputForm', function(){
		return {
			restrict	: 'E',
			templateUrl : '/html/templates/inputForm.html',
			controller 	: 'ScannerCtrl',
			controllerAs: 'scanner'
		};
	});

	app.directive('resultsTable', function(){
		return {
			restrict	: 'E',
			templateUrl	: '/html/templates/resultsTable.html',
			controller 	: 'ScannerCtrl',
			controllerAs: 'scanner'
		};
	});

})();