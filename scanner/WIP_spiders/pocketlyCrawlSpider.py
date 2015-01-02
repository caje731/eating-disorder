from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#Done.
#Pocketly
#start_url =
# http://pocketly.com/search?keywords=peanuts+deluxe+cafe&location=san+jose&longitude=&latitude=


class PocketlyCrawlSpider(CrawlSpider):

	name = 'pocketlyCrawlSpider'

	def __init__(self,query,location,state, *args, **kwargs):
		
		location 	= location.replace(' ','-')
		query 		= query.replace(' ','-')
		self.rules = (Rule(	LinkExtractor(allow=('/biz/'+query+'-'+location+'-'+state+'/*')),
							callback='parse_item',
							follow = True),)
		super(PocketlyCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['pocketly.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://pocketly.com/search?keywords='+query+'&location='+location+'&longitude=&latitude=']
		

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="storeName"]/text()')
		l.add_xpath('address','//*[@id="address1"]/text()')
		l.add_xpath('address','//*[@id="addressCity"]/text()')
		l.add_xpath('address','//*[@id="addressState"]/text()')
		l.add_xpath('address','//*[@id="addressZip"]/text()')
		l.add_xpath('phone','//*[@id="phoneNumber"]/text()')
		l.add_value('websource', 'pocketly')
		return l.load_item()