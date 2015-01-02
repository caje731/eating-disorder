from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE Perfectly.
#start_url =
# http://www.yellowbot.com/search?lat=&long=&q=peanuts+deluxe+cafe&place=san+jose



class YellowBotCrawlSpider(CrawlSpider):

	name = 'yellowbotCrawlSpider'

	def __init__(self, query,  city,state, *args, **kwargs):
		query = query.replace(' ','-')
		city = city.replace(' ','-')
		self.rules = (Rule(	LinkExtractor(allow=('/'+query+'-'+city+'-'+state+'*')),
							callback='parse_item',
							follow = True),)
		super(YellowBotCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.yellowbot.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.yellowbot.com/search?lat=&long=&q='+query+'&place='+city]
		

	def parse_item(self,response):

		l = ItemLoader(item=BusinessInfoItem(),response=response)
		l.add_xpath('name','//*[@id="info-container"]/div[1]/h1/text()')
		l.add_xpath('address','//*[@id="info-container"]/div[1]/dl/dd[1]/span[1]/text()')
		l.add_xpath('address','//*[@id="info-container"]/div[1]/dl/dd[1]/span[2]/text()')
		l.add_xpath('address','//*[@id="info-container"]/div[1]/dl/dd[1]/span[3]/text()')
		l.add_xpath('address','//*[@id="info-container"]/div[1]/dl/dd[1]/span[4]/text()')
		l.add_value('websource', 'yellowbot')
		return l.load_item()