(function(){
	'use strict';

	var app = angular.module('scanner');

	app.factory('scannerAPI', ['$http', '$q', scannerAPI]);

	function scannerAPI($http, $q){

		self.jobs = {};

		/* Triggers a new search/crawl on the server */
		var beginSearch = function(name, city, location, area){
			var scanner_url	= window.location.protocol+"//"+window.location.hostname+':9000/scan';
			var POLL_TIME_MS= 2000;
			self.jobs = {}; //reset

			name = name || '';
			city = city || '';
			location = location ||'';
			area = area || '';

			var reqdata = {
				"query"		: name,
				"city"      : city,
				"location" 	: location,
				"area"		: area
			};

			var deferred = $q.defer();

			$http.post(scanner_url, reqdata)
			.then(function(resp){
				var results = resp.data.results;
				for(var index=0; index<results.length; index++){
					self.jobs[results[index]["jobid"]] = { websource : results[index]["websource"], status : "pending" };
				}
				deferred.resolve(self.jobs);

			}, function(err){
				console.log(JSON.stringify(err));
				deferred.reject(err);
			});

			return deferred.promise;
		};

		/* For all pending jobs, fetches the status from the server */
		var getJobStatus = function(jobIds){
			var scanner_url	= window.location.protocol+"//"+window.location.hostname+':9000/scanstatus';
			var POLL_TIME_MS= 2000;

			var deferred = $q.defer();

			$http.get(scanner_url+'?jobIds='+jobIds)
				.then(function(resp){
					for(var i =0; i< resp.data.pending.length; i++){
						var id = resp.data.pending[i];
						self.jobs[id].status = "pending";
					}
					for(var i =0; i< resp.data.error.length; i++){
						var id = resp.data.error[i];
						self.jobs[id].status = "error";
					}
					for(var i =0; i< resp.data.empty.length; i++){
						var id = resp.data.empty[i];
						self.jobs[id].status = "empty";
					}
					for(var i=0; i< resp.data.finished.length; i++){
						var job = resp.data.finished[i];
						var keys= Object.keys(self.jobs);
						for(var j =0; j<keys.length; j++){
							if(self.jobs[keys[j]].websource === job.websource){
								self.jobs[keys[j]] = job;
								self.jobs[keys[j]].status = "finished";
							};	
						}
					}
					deferred.resolve(self.jobs);
				}, function(err){
					console.log(JSON.stringify(err));
					deferred.reject(err);
				});

			return deferred.promise;
		};

		return {
			beginSearch	: beginSearch,
			getJobStatus: getJobStatus
		};
	};
})();