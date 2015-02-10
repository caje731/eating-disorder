(function(){
	'use strict';

	var app = angular.module('scanner');

	app.controller('ScannerCtrl', ['scannerAPI', ScannerCtrl]);

	function ScannerCtrl(scannerAPI){
		var vm = this;

		vm.input = {};
		vm.finished_items 	= [];
		vm.error_items		= [];
		vm.pending_items	= [];
		vm.empty_items		= [];

		vm.getFinishedItems = function(){
			return vm.finished_items;
		};
		vm.getErrorItems = function(){
			return vm.error_items;
		};
		vm.getPendingItems = function(){
			return vm.pending_items;
		};
		vm.getEmptyItems = function(){
			return vm.empty_items;
		};

		vm.setFinishedItems = function(items){
			vm.finished_items = items;
		};
		vm.setErrorItems = function(items){
			vm.error_items = items;
		};
		vm.setPendingItems = function(items){
			vm.pending_items = items;
		};
		vm.setEmptyItems = function(items){
			vm.empty_items = items;
		};

		vm.segregateJobs = function(jobs){
			var keys = Object.keys(jobs);
			var temp_pending 	= [];
			var temp_error 		= [];
			var temp_empty 		= [];
			var temp_finished 	= [];
			
			for(var i =0; i < keys.length; i++){
				jobs[keys[i]]["jobid"] = keys[i];
				var status = jobs[keys[i]].status;

				if(status === 'pending'){
					temp_pending.push(jobs[keys[i]]);
				}
				else if(status === 'error'){
					temp_error.push(jobs[keys[i]]);
				}
				else if(status === 'empty'){
					temp_empty.push(jobs[keys[i]]);
				}
				else if(status === 'finished'){
					temp_finished.push(jobs[keys[i]]);
				}
			}

			vm.setPendingItems(temp_pending);
			vm.setErrorItems(temp_error);
			vm.setEmptyItems(temp_empty);
			vm.setFinishedItems(temp_finished);
		};

		vm.startNewSearch = function(){

			vm.jobs 			= {};

			vm.finished_items 	= [];
			vm.error_items		= [];
			vm.pending_items	= [];
			vm.empty_items		= [];

			scannerAPI.beginSearch( vm.input.name, vm.input.city, vm.input.location, vm.input.area )
			.then(function(jobs){

				// Segregate jobs according to status
				vm.segregateJobs(jobs);

				// Wait for server to finish pending jobs, and query again
				window.setTimeout(function(){
					var pendingIds = [];
					for (var i=0; i<vm.pending_items.length; i++){
						pendingIds.push(vm.pending_items[i]["jobid"]);
					}
					scannerAPI.getJobStatus(pendingIds)
					.then(function(jobs){
						vm.segregateJobs(jobs);
						vm.monitorStatus();
					}, 
					function(err){
						console.log(JSON.stringify(err));
					});
				}, POLL_TIME_MS);
			}, function(err){
				console.log(JSON.stringify(err));
			});
		};

		vm.monitorStatus = function(){

			// If there's nothing pending, stop the monitoring
			if(vm.pending_items.length<1){
				return;
			}
			else{
				// Wait for server to finish pending jobs, and query again
				window.setTimeout(function(){
					var pendingIds = [];
					for (var i=0; i<vm.pending_items.length; i++){
						pendingIds.push(vm.pending_items[i]["jobid"]);
					}
					scannerAPI.getJobStatus(pendingIds)
					.then(function(jobs){
						vm.segregateJobs(jobs);
						vm.monitorStatus();
					}, 
					function(err){
						console.log(JSON.stringify(err));
					});
				}, POLL_TIME_MS);
			}
		};

		vm.isSearchInProgress = function(){
			return vm.getPendingItems().length>0;
		};
	};
})();