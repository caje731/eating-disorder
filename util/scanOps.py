#!/usr/bin/env python

import fileLogger 		# for custom logging (I'm not relying on Flask's in-app logger)
import subprocess		# for invocation of custom scrapy commands (assumed to be installed)
import os				# 
import glob				# filename globbing to retrieve scraped items
import json, re			# for string processing
import urllib2			# for invoking the scrapyd server APIs
import sys, traceback 	# exception handling


def replace_unicode_marker(matchobj):
	return '"'+matchobj.group(2)+'"'		

# Cleans unicode markers and single quotes from a string
def clean_string(unclean_str):
	unclean_str = unclean_str.replace("\\xa0", "")  # remove non-breaking space \xa0 if present
	unclean_str = unclean_str.replace("'", "\"")	# Client-side js won't like single quote while loading json
	unclean_str = unclean_str.replace('{u"', '{"')	# u is unicode marker
	unclean_str = unclean_str.replace(': u"', ': "')
	unclean_str = unclean_str.replace('[u"', '["')
	clean_str 	= unclean_str.replace(', u"', ', "')
	return clean_str


def trigger_all(query, city, area, location, state, pincode, category):
	logger = fileLogger.get_file_logger()
	logger.debug('[SCOP] Triggering scrapy allcrawl...')
	return subprocess.check_output(['scrapy', 'allcrawl', 'query='+query, 'city='+city, 'area='+area, 'location='+location, 'state='+state, 'pincode='+pincode,'category='+category], stderr=subprocess.STDOUT)

def get_pending_results(jobIds):
	
	SCRAPYD_JOBLIST_URL = 'http://localhost:6800/listjobs.json?project=scanner'
	SCRAPYD_ITEMS_PATH	= '/var/www/html/scanner/items/scanner/*/*'
	#SCRAPYD_ITEMS_PATH	= '/items/scanner/*/*'
	pending_jobIds		= []	# jobs that are either still running or yet to be scheduled
	finished_jobItems	= []	# items scraped from finished crawls
	empty_crawls		= []	# spiders that returned nothing after crawling
	error_jobs			= []	# Jobs whose output could not be obtained
	
	logger = fileLogger.get_file_logger()
	
	request				= urllib2.Request(SCRAPYD_JOBLIST_URL)
	response			= urllib2.urlopen(request)
	jobstats			= json.loads(response.read())
	

	itemFiles			= {}	
	for jobId in jobIds:
		for filename in glob.iglob(SCRAPYD_ITEMS_PATH):  # The iterator will also list unwanted files, so filter them
			if filename.endswith(jobId+'.jl'):
				itemFiles[jobId] = filename
				
	for fin_job in jobstats['finished']:
		if fin_job["id"] in jobIds:
			curr_job = str(fin_job["id"]).replace("u'", "'")
			
			if curr_job not in itemFiles:
				error_jobs.append(curr_job)
				continue
			
			with open(itemFiles[curr_job], 'r') as itemFile:
				lines_read		= 0
				go_to_next_line = True 	# Go to next line if Item encountered has only one key ("websource" is present by default)
				
				while go_to_next_line:
					itemstr = itemFile.readline()
					logger.debug('Line read: '+ itemstr)
					if len(itemstr) > 0:
						lines_read += 1
						# Convert the item string to a JSON object
						item 		= json.loads(itemstr)
						itemkeys 	= item.keys()
						if "websource" in itemkeys :

							if len(itemkeys) == 1:
								# Only websource was present, nothing scraped
								empty_crawls.append(curr_job)
								go_to_next_line = False
								continue

							# Fill/Insert missing keys with placeholder
							# And join the list-elements of what's present into a string
							
							item["websource"] = ' '.join(item["websource"])
							
							if "name" not in itemkeys:
								item["name"] = 'Not found'
							else:
								item["name"] = ' '.join(item["name"])
								
							if "address" not in itemkeys:
								item["address"] = 'Not found'
							else:
								item["address"] = ' '.join(item["address"])
							
							if "phone" not in itemkeys:
								item["phone"] = 'Not found'
							else:
								item["phone"] = ' '.join(item["phone"])
								
							if "timings" not in itemkeys:
								item["timings"] = 'Not found'
							else:
								item["timings"] = ' '.join(item["timings"])
								
							finished_jobItems.append(item)
							go_to_next_line = False 
							
						else:
							# Current line does not contain item of interest, go to next line
							pass
					else:
						# EOF reached, let python close the file
						if lines_read == 0:
							#empty_crawls.append(fin_job["spider"].replace("CrawlSpider", ""))
							empty_crawls.append(curr_job)
						go_to_next_line = False
		else:
			# Do nothing, this job is not among the ones requested by the user
			pass
		
	for pend_job in jobstats['pending']:
		if pend_job["id"] in jobIds:
			pending_jobIds.append(pend_job["id"])
	
	for running_job in jobstats['running']:
		if running_job["id"] in jobIds:
			pending_jobIds.append(running_job["id"])
	
	return 	{"pending":pending_jobIds, "finished":finished_jobItems, "empty":empty_crawls, "error":error_jobs}
	

def start_new_scan(request):
	
	logger 	= fileLogger.get_file_logger()
	reqData = request.json
	
	query = city = area = location = state = pincode = category = ""

	if "query" in reqData:
		query	= reqData["query"	]
	
	if "city" in reqData:
		city	= reqData["city"	]

	if "area" in reqData:
		area	= reqData["area"	]
	
	if "location" in reqData:
		location= reqData["location"]
	
	if "state" in reqData:
		state	= reqData["state"	]

	if "pincode" in reqData:
		pincode = reqData["pincode"	]

	if "category" in reqData:
		category= reqData["category"]

	results = trigger_all(query, city, area, location, state, pincode, category)

	results = clean_string(results)
	
	logger.debug('[SCOP] Trigger results (processed): '+results)
	return results

def get_job_status(request):

	logger 	= fileLogger.get_file_logger()
	reqData = request.args.to_dict()

	if "jobIds" in reqData:
		jobIds	= reqData["jobIds"	].split(",")
		results = get_pending_results(jobIds)
		results = clean_string(str(results))
		logger.debug('[SCOP] Job Status Results (processed): ' + results)
		return results

	else:
		return '{"execFault": "No job ids specified"}'
