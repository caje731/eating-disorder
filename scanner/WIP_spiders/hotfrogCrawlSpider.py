from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE.
#Hotfrog.
#start_url=
#  http://www.hotfrog.com/Products/Peanuts/CA/San-Jose
#limit:
#  http://www.hotfrog.com/Companies/Peanuts-Deluxe-Cafe

class HotfrogCrawlSpider(CrawlSpider):

	name = 'hotfrogCrawlSpider'

	def __init__(self, query, state, city, *args, **kwargs):
		
		query = query.replace(' ','-')
		self.rules = (Rule(	LinkExtractor(allow=('/Companies/'+query)), 
							callback='parse_item',
							follow = True),)

		super(HotfrogCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.hotfrog.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.hotfrog.com/Products/'+query+'/'+state+'/'+city]

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('company','//*[@id="content"]/div[2]/div[1]/h1/text()')
		l.add_xpath('address','//*[@id="content"]/div[2]/div[4]/text()[1]')
		l.add_xpath('phone','//*[@id="content"]/div[2]/div[4]/text()[2]')
		l.add_value('websource', 'hotfrog')
		return l.load_item()