from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

class YelpCrawlSpider(CrawlSpider):
	name = 'yelpCrawlSpider'

	def __init__(self, query, city, state, *args, **kwargs):
		
		query = query.replace(' ','-')
		city = city.replace(' ','-')
		self.rules = (Rule(	LinkExtractor(allow=(r'/biz/'+query+'-'+ city+'-',
												 r'/map/'+query+'-'+ city+'-')),
							callback='parse_item'),)
		self.allowed_domains = ['www.yelp.com']
		super(YelpCrawlSpider, self).__init__(*args, **kwargs)
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.yelp.com/search?find_desc='+query+'&find_loc='+city+'%2C+'+state]

	def parse_item(self,response):
		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="wrap"]/div[3]/div[1]/div/div[2]/div[1]/h1/text()')
		l.add_xpath('address', '//*[@id="super-container"]/div[3]/div/div/div/div[1]/div/div/div/form/div[3]/div/div/div[2]/address/text()')
		l.add_xpath('timings','//*[@id="super-container"]/div/div/div[2]/div[1]/div[1]/ul/li[1]/div[2]/dl/dd/span[1]')
		l.add_value('websource', 'yelp')
		return l.load_item()
