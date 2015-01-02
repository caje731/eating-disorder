from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#Done. Check json file generated. If the file is non empty, there exist company/companies with the searched name..
#ecplaza.net
#start_url:
# http://www.ecplaza.net/tamo--company.html

class ECPlazaCrawlSpider(CrawlSpider):

	name = 'ecplazaCrawlSpider'

	def __init__(self, query, *args, **kwargs):
		
		query = query.replace(' ','-')
		self.rules = (Rule(	LinkExtractor(	allow=(	'en.ecplaza.net'),
											deny=(	'en.ecplaza.net/gps*',
													'en.ecplaza.net/city*',
													'en.ecplaza.net/bus*',
													'en.ecplaza.net/audio*',
													'en.ecplaza.net/led*',
													'en.ecplaza.net/about*',
													'en.ecplaza.net/tour*',
													'en.ecplaza.net/multi*',
													'en.ecplaza.net/self*',
													'en.ecplaza.net/product*',
													'en.ecplaza.net/auto*')
										),
							callback='parse_item',
							follow = True),)
							
		super(ECPlazaCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['ecplaza.net']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.ecplaza.net/'+query+'--company.html']
		
	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','/html/body/div[3]/div[1]/table[1]/text()')
		l.add_value('websource', 'ecplaza')
		return l.load_item()
		