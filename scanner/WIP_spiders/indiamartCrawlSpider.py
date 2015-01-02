from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE.
#IndiaMart
#start_url="http://dir.indiamart.com/cgi/catprdsearch.mp?ss=khandela+electronika"
#query="khandela-electronika"

class IndiaMartCrawlSpider(CrawlSpider):

	name = 'indiamartCrawlSpider'

	def __init__(self, query, *args, **kwargs):
		query = query.replace(' ','-')
		self.rules = (Rule(	LinkExtractor(allow=('/'+query+'*')), 
							callback='parse_item',
							follow = True),
						)
		super(IndiaMartCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.indiamart.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://dir.indiamart.com/cgi/catprdsearch.mp?ss='+query]
		

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/span[3]/h1/text()')
		l.add_xpath('address','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/div[3]/span[1]/text()')
		l.add_xpath('address','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/div[3]/span[2]/text()')
		l.add_xpath('address','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/div[3]/span[4]/text()')
		l.add_xpath('address','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/div[3]/span[3]/text()')
		l.add_xpath('phone','//*[@id="main_div"]/div[6]/div[3]/div[4]/div[1]/span[5]/text()')
		l.add_value('websource', 'indiamart')
		return l.load_item()