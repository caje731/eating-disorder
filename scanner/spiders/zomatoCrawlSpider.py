# -*- coding: utf-8 -*-

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader

from scanner.items import BusinessInfoItem

''' 
	Requires input validation for area field. Not always necessary to be entered by the user. In such case, send '' as parameter since the spider needs it.
	On the scrapy CLI, type : 
	scrapy crawl zomatoCrawlSpider -a city="mumbai" -a location="bandra west" -a area="pali hill" -a query="stomach" -a	start_url= "http://www.zomato.com/mumbai/restaurants?q=stomach"
'''

class ZomatoCrawlSpider(CrawlSpider):
	name 			= 'zomatoCrawlSpider'
	allowed_domains = ['www.zomato.com']

	
	def __init__(self, city, location, area, query, *args, **kwargs):
		location_parts 	= location.split(' ')
		location_1		= location_parts[0].lower()
				
		query 		= query.replace(' ','-').lower()
		location 	= location.replace(' ','-').lower()
		city		= city.lower()

		if area is not '':
			area = area.replace(' ','-').lower()
			area = area+'-'
		
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls	= [	'http://www.zomato.com/'+city+'/restaurants?q='+query]
		
		self.rules = (
			Rule(	LinkExtractor(	allow=	(	'.*/'+city+'/'+query+'-'+area+location+'$',
												'.*/'+city+'/'+query+'-'+'.*'+location+'$',
												'.*/'+city+'/'+query+'-'+'.*'+location+'.*',
												'.*/'+city+'/'+query+'-'+'.*'+location_1+'$'),
									deny=	(	'.*/menu.*',
												'.*/map.*',
												'.*/review.*',
												'.*/info.*',
												'.*/photo.*',
												'.*?sort=[a-z]{2}',
												'.*?lang=.*')
									),
					callback= 'parse_item',
					follow	= True
				),
		)
		super(ZomatoCrawlSpider, self).__init__(*args, **kwargs)
		
	def parse_item(self, response):
		l = ItemLoader(item = BusinessInfoItem(),response = response)
		
		l.add_xpath('name', '//h1[@class="res-name left"]/a/span/text()')
		
		# Multiple lines of the address, mixed with some span tags
		l.add_xpath('address', '//div[@itemtype="http://schema.org/PostalAddress"]/text()[1]')					
		l.add_xpath('address', '//div[@itemtype="http://schema.org/PostalAddress"]/span[1]/text()')
		l.add_xpath('address', '//div[@itemtype="http://schema.org/PostalAddress"]/text()[2]')
		l.add_xpath('address', '//div[@itemtype="http://schema.org/PostalAddress"]/span[2]/text()')
		
		
		# There could be multiple phone numbers, let them be appended by the "phone"'s Input Processor
		l.add_xpath('phone','//*[@id="phoneNoString"]/div/span/span[1]/span/text()')
		l.add_xpath('phone','//*[@id="phoneNoString"]/div/span/span[2]/span/text()')
		
		l.add_xpath('timings','//span[@class="res-info-timings"]/div/div[1]/div[2]/span[1]/text()')
		l.add_xpath('cuisine','//a[@itemprop="servesCuisine"]/text()')
		l.add_xpath('cost', '//span[@itemprop="priceRange"]/text()')
		l.add_xpath('menus', '//div[@class="menu-preview__item"]/a')

		l.add_value('websource', 'zomato')
		return  l.load_item()
