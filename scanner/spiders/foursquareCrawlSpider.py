from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE.
#Foursquare
#start_url="https://foursquare.com/explore?mode=url&near=San%20Jose&q=peanuts%20deluxe%20cafe"
#queries need to be as exact as possible.


class FoursquareCrawlSpider(CrawlSpider):
	name = 'foursquareCrawlSpider'

	def __init__(self, query, city, *args, **kwargs):
		query 		= query.replace(' ','-')
				
		self.rules = (Rule(	LinkExtractor(allow=(r'/v/'+query+'/*')),
							callback='parse_item'),)
		super(FoursquareCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['foursquare.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['https://foursquare.com/explore?mode=url&near='+city+'&q='+query]

	def parse_item(self,response):
		l = ItemLoader(item = BusinessInfoItem(),response = response)
		
		# I couldn't find cost and cuisine elements
		l.add_xpath('name','//div[@class="venueNameSection"]/span/text()')
		l.add_xpath('phone','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/span/text()')
		l.add_xpath('address','//*[@itemtype="http://schema.org/PostalAddress"]/span/text()')
		l.add_xpath('address','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/span[1]/text()')
		l.add_xpath('address','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/span[2]/text()')
		l.add_xpath('address','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/span[3]/text()')
		l.add_xpath('address','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/span[4]/text()')
		l.add_xpath('address','//*[@id="container"]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div/text()[3]/text()')
		l.add_value('websource', 'foursquare')
		# Couldn't find any menu images on foursquare
		return l.load_item()
