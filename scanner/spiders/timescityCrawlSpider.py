from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE.
#Timescity
#start_url="http://timescity.com/mumbai/search?searchname=vihang%27s%20inn"
#limit: http://timescity.com/mumbai/thane-west/north-indian-restaurant-palm-court/73059

class TimesCityCrawlSpider(CrawlSpider):

	name = 'timescityCrawlSpider'

	def __init__(self, city, location, query, *args, **kwargs):
		
		location_1  = location.split(' ')[0]
		location 	= location.replace(' ','-')
		query 		= query.replace(' ','-')
		
		self.rules = (Rule(	LinkExtractor(	allow=(	'/'+city+'/'+location+'/.*'+query+'*',
													'/'+city+'/'+location_1+'.*/.*'+query+'*'),
											deny =(	'.*reviews.*',
													'.*menu.*')
										),
							callback='parse_item',
							follow = True),)
		super(TimesCityCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['timescity.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://timescity.com/'+city+'/search?searchname='+query]
		

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="restaurantDetailDiv"]/div[1]/div/div[1]/div[1]/h1/a/text()')
		l.add_xpath('address','//*[@id="restaurantDetailDiv"]/div[2]/div/div[1]/div[1]/span/span/text()')
		l.add_xpath('phone','//*[@id="collapsesix"]/div/div/div/div/span/a/text()')
		l.add_value('websource', 'timescity')
		return l.load_item()
		
		#//*[@id="restaurantDetailDiv"]/div[2]/div/div[1]/div[1]/span[2]
		#//*[@id="restaurantDetailDiv"]/div[2]/div/div[1]/div[1]/span/text()

		
