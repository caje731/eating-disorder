from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem


#Input: location="locality in the city, separated by -, if spaces exists in name. query="name of the restaurant. - for each space.""
# start_url="search url" --> start_url="http://www.burrp.com/mumbai/search.html?q=pop%20tates"

class BurrpCrawlSpider(CrawlSpider):
	name = 'burrpCrawlSpider'
	allowed_domains = ['www.burrp.com']
	start_urls		= ['http://www.burrp.com']
	
	#replace spaces with - in query and location, while passing as parameter.
	#replace spaces with %20 while passing start_url as parameter.

	def __init__(self, query, city, location, *args, **kwargs):
		query 		= query.replace(' ','-')
		location 	= location.replace(' ','-')
		city 		= city.replace(' ','-')
		
		self.rules 	= (Rule(LinkExtractor(allow=('burrp.com/'+city+'/'+query+'-'+location+'*')),
							callback='parse_item',
							follow=True),)
		
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.burrp.com/'+city+'/search.html?q='+query]
		super(BurrpCrawlSpider, self).__init__(*args, **kwargs)

	def parse_item(self,response):
		l = ItemLoader(item = BusinessInfoItem(),response = response)
		
		l.add_xpath('name', '//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/span/h1/text()')
		l.add_xpath('name','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/span/p/text()')
		
		l.add_xpath('phone','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/div/ul/li[1]/strong/text()')
		l.add_xpath('address','//*[@id="listings-details"]/section[2]/div/div[1]/div[1]/div/ul/li[2]/text()')
		
		l.add_value('websource', 'burrp')
		return l.load_item()