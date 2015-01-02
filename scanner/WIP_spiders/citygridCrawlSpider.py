
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE. But Pointless. Extra Zipcode Input required. End result is the name of the listing alone.
#CityGrid.
#start_url="http://www.citygrid.com/places/search?what=peanuts+deluxe+cafe&where=95112"
#take pincode also as input, for the start_url.
#take city also as input

class CityGridCrawlSpider(CrawlSpider):

	name = 'citygridCrawlSpider'

	def __init__(self, query, city, pincode, *args, **kwargs):
		query 	= query.replace(' ','-')
		city 	= city.replace(' ','-')
		self.rules = (Rule(	LinkExtractor(allow=('/'+query+'-'+city)), 
							callback='parse_item',
							follow = True),)
		super(CityGridCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.citygrid.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.citygrid.com/places/search?what='+query+'&where='+pincode]

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="place_header"]/div[2]/h2/text()')
		l.add_xpath('address','//*[@id="place_header"]/div[2]/p/span[1]/br/text()')
		l.add_xpath('phone','//*[@id="place_header"]/div[2]/p[2]/span[2]/text()')
		l.add_value('websource', 'citygrid')
		return l.load_item()