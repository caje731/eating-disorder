from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem


#DONE. Perfectly.
#exportersindia.com
#start_url:
# http://www.exportersindia.com/search.php?term=khandela+electronika&srch_catg_ty=comp
#limit:
# http://www.exportersindia.com/ptagiselectronika/


class ExportersIndiaCrawlSpider(CrawlSpider):

	name = 'exportersindiaCrawlSpider'

	def __init__(self, query, category, *args, **kwargs):
		query = query.replace(' ','+')
		self.rules = (Rule(	LinkExtractor(allow=('/'+query+'/*')),
							callback='parse_item',
							follow = True
							),
						)
		super(ExportersIndiaCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['exportersindia.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.exportersindia.com/search.php?term='+query+'&srch_catg_ty='+category]
			

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="logo"]/section/ul/li/h1/text()')
		l.add_xpath('address','//*[@id="thinColumn"]/section[2]/nav/p[1]/text()')
		l.add_xpath('address','//*[@id="thinColumn"]/section[2]/nav/p[2]/text()')

		#l.add_xpath('company_info','//*[@id="wideColumn"]/section[1]/nav/p/text()')
		#l.add_xpath('contact_person','//*[@id="thinColumn"]/section[2]/nav/b/text()')
		#l.add_xpath('fax','//*[@id="thinColumn"]/section[2]/nav/p[3]/text()')
		#l.add_xpath('business_type','//*[@id="wideColumn"]/section[2]/nav/p[1]/span[3]/text()')
		#l.add_xpath('company_turnover','//*[@id="wideColumn"]/section[2]/nav/p[3]/span[3]/text()')
		#l.add_xpath('markets','//*[@id="wideColumn"]/section[2]/nav/p[4]/span[3]/text()')
		l.add_value('websource', 'exportersindia')
		return l.load_item()