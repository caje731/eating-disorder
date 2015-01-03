#!/usr/bin/env python
import cgi, os, urllib2, json, subprocess, glob

def trigger_all(query, city, area, location, state, pincode, category):
	#return os.system('"scrapy allcrawl query="'+query+'" city="'+city+'" area="'+area+'" location="'+location+'" state="'+state+'" pincode="'+pincode+'" category="'+category+'""')
	#subprocess.call ([	'scrapy', 'allcrawl', 'query='+query, 'city='+city, 'area='+area, 'location='+location, 'state='+state, 'pincode='+pincode,'category='+category])
	return subprocess.check_output(['scrapy', 'allcrawl', 'query='+query, 'city='+city, 'area='+area, 'location='+location, 'state='+state, 'pincode='+pincode,'category='+category], stderr=subprocess.STDOUT)
	
def get_pending_results(jobIds):
	
	SCRAPYD_JOBLIST_URL 	= 'http://localhost:6800/listjobs.json?project=scanner'
	SCRAPYD_ITEMS_PATH	= '../items/scanner/*/*'
	pending_jobIds		= []	# jobs that are either still running or yet to be scheduled
	finished_jobItems	= []	# items scraped from finished crawls
	empty_crawls		= []	# spiders that returned nothing after crawling
	error_jobs		= []	# Jobs whose output could not be obtained
	
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
					if len(itemstr) > 0:
						lines_read += 1
						# Convert the item string to a JSON object
						item 		= json.loads(itemstr)
						itemkeys 	= item.keys()
						if "websource" in itemkeys and len(itemkeys) > 1: # There are keys apart from websource
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
							empty_crawls.append(fin_job["spider"].replace("CrawlSpider", ""))
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
	
	return {"pending": pending_jobIds, "finished": finished_jobItems, "empty": empty_crawls, "error": error_jobs}
	
		
	
if __name__ == "__main__":
	
	# HTTP headers
	print 'HTTP/1.1 200 OK'
	print 'Content-type: text/html'
	print 'Access-Control-Allow-Origin: *'		# for Cross-Origin Resource Sharing
	print
	
	
	# Check the action specified in the POST data and do the right thing
	fieldStore 	= cgi.FieldStorage()
	action 		= fieldStore['action'].value
	
	query 	= city = area = location = state = pincode = category = ""
	jobIds 	= []

	if "query" in fieldStore:
		query	= fieldStore["query"	].value
	if "city" in fieldStore:
		city	= fieldStore["city"	 	].value
	if "area" in fieldStore:
		area	= fieldStore["area"	 	].value
	if "location" in fieldStore:
		location= fieldStore["location"	].value
	if "state" in fieldStore:
		state	= fieldStore["state"	].value
	if "pincode" in fieldStore:
		pincode = fieldStore["pincode"	].value
	if "category" in fieldStore:
		category= fieldStore["category"	].value
	if "jobIds" in fieldStore:
		jobIds	= fieldStore["jobIds"	].value.split(",")

	if action=="TRIGGER":
		print trigger_all(query, city, area, location, state, pincode, category)
	
	elif action=="RECEIVE" : 
		print str(get_pending_results(jobIds))
	
	else:
		pass
