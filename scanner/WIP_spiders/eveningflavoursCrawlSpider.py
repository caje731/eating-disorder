from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

# REQUEST BEING FILTERED.
#EveningFlavours
#start_url=
# http://eveningflavors.com/Restaurants-Pubs-GenericSearch-Process/Restaurants-Pubs-Hotels-Lounge-Search-India.jsp?city=Mumbai&checkRequestPage=quickSearch&inputForQuickSearch=stomach&placeLookingInput=bandra+west
#limit=
# http://eveningflavors.com/Stomach/Mumbai/6747/

class EveningFlavoursCrawlSpider(CrawlSpider):
	name = 'eveningflavoursCrawlSpider'

	def __init__(self, city, location, query, *args, **kwargs):
		location = location.replace(' ', '+')
		query	 = query.replace(' ', '+')
		self.rules = (Rule(	LinkExtractor(allow=(r'/'+query+'/'+location+'/*')), 
							callback='parse_item',
							follow = True),)
		super(EveningFlavoursCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.eveningflavours.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self_start_urls = ['http://eveningflavors.com/Restaurants-Pubs-GenericSearch-Process/Restaurants-Pubs-Hotels-Lounge-Search-India.jsp?city='+city+'&checkRequestPage=quickSearch&inputForQuickSearch='+query+'&placeLookingInput='+location]
		

	def parse_item(self,response):
		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('phone','//*[@id="Prof-Quickview-Desc"]/p/text()')
		l.add_xpath('address','//*[@id="profiletab1"]/p/font/text()')
		l.add_xpath('timings','//*[@id="Prof-Quickview-Heading"]/p/font/b')
		l.add_xpath('name','//*[@id="table48"]/tbody/tr[2]/td[1]/h1/span/a/text()')
		l.add_value('websource', 'eveningflavours')
		return l.load_item()
