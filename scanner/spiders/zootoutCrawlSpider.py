from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

import re

#start_url="http://www.zootout.com/mumbai/stomach-bandra-west-4162"
#location="mumbai"

class ZootoutCrawlSpider(CrawlSpider):

	name = 'zootoutCrawlSpider'

	def __init__(self, query, city, location, *args, **kwargs):
		
		location_parts 	= location.split(' ')
		location_1 		= location_parts[0]
		
		location 	= location.replace(' ','-')
		query 		= query.replace(' ','-')
		self.rules = (Rule(	LinkExtractor(	allow=(	'/'+query.replace('\'', '-')+'-'+location+'*',
													'/'+query.replace('\'', '-')+'-'+location_1+'*'),
											deny=(	'/dishes',
													'/map',
													'/overview',
													'/photos')),
							callback='parse_item',
							follow = True),)
		super(ZootoutCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.zootout.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = [	'http://www.zootout.com/'+city+'/'+query.replace('\'', '')+'-'+location,
								'http://www.zootout.com/'+city+'/'+query.replace('\'', ''),
								'http://www.zootout.com/'+city+'/restaurant/'+query.replace('\'', '')]
		

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name',		'/html/body/div[5]/div[1]/div/div[2]/div[1]/h1/span[1]/text()')
		l.add_xpath('address',	'//*[@id="port"]/div/div[1]/div/div[1]/div/text()')
		l.add_xpath('address',	'//*[@id="port"]/div/div[1]/div/div[1]/a/text()')
		l.add_xpath('timings',	'//*[@id="port"]/div[2]/div[1]/div/div[11]/div[1]/span[2]/text()')
		l.add_xpath('phone',	'/html/body/div[5]/div[1]/div/div[2]/div[1]/div[3]/@onclick')
		l.add_xpath('cuisine',	'//*[@id="port"]/div[2]/div[1]/div/div[5]/span/text()')
		l.add_xpath('cost',		'//div[@itemprop="priceRange"]/text()')
		# Couldn't find any menu images on foursquare

		l.add_value('websource', 'zootout')
		
		scraped_item = l.load_item()
		if 'phone' in scraped_item:
			matchObj  = re.search("'(.*?)'", scraped_item['phone'][0])
			if matchObj:
				scraped_item['phone'] = matchObj.group(1)
		
		return scraped_item
		
		