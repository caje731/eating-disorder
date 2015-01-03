#!/usr/bin/env python
from __future__ import print_function
from multiprocessing import Process, Queue
import urllib, urllib2
import sys

SCRAPYD_SCHEDULE_URL	= 'http://localhost:6800/schedule.json'
PROJECT_NAME			= 'scanner'

def crawl(output_queue, spider="", city="", area="", location="", query="", category="", state="", pincode=""):
	values 	= {	'project': PROJECT_NAME,
				'spider': spider,
				'city': city,
				'area': area,
				'location': location,
				'query': query,
				'category': category,
				'state': state,
				'pincode': pincode
				}

	data 	= urllib.urlencode(values)
	request	= urllib2.Request(SCRAPYD_SCHEDULE_URL, data)
	response= urllib2.urlopen(request)
	if output_queue == None:
		print(response.read())
	else:
		output_queue.put(response.read())
	
def crawlproxy(output_queue, list):
	crawl(output_queue, *list)

	
def distribute(job_configs):
	if len(job_configs) < 1:
		print('[distribute.py][Usage_Error] No recognisable arguments provided.', file=sys.stderr)
		
	else:
		# For each job, create a queue to store its output
		queues 	= [Queue() for job in job_configs]

		# For each job, create a process that invokes crawlproxy
		jobs	= [Process(target=crawlproxy, args=[queues[i], conf[:] ]) for i,conf in enumerate(job_configs)]
		for job in jobs: job.start() #start all of them
		for job in jobs: job.join()  #wait for all to finish
		
		return [queue.get().strip() for queue in queues]
		
	
def parse_args():
	spider_names = []
	
	# Arguments needed by the spiders.
	city = area = location = query = category = state = pincode = ""
	
	for arg in sys.argv[1:]:
		key, value = arg.split('=')
		valueLwr = value.lower()
		if "city"==key:
			city = valueLwr
		elif "area"==key:
			area = valueLwr
		elif "location"==key:
			location = valueLwr
		elif "query"==key:
			query = valueLwr
		elif "category"==key:
			category = valueLwr
		elif "state"==key:
			state = valueLwr
		elif "pincode"==key:
			pincode = valueLwr
		elif "spider"==key:
			spider_names.append(value)
		else:
			pass
	
	list_of_arglists = []
	for spider in spider_names:
		list_of_arglists.append([spider, city, area, location, query, category, state, pincode])
	
	return list_of_arglists
	
if __name__ == '__main__':
	print(distribute(parse_args()))
