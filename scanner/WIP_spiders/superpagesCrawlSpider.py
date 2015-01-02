from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem


# FILTERED OFFSITE REQUEST.
#SuperPages
#start_url=
# http://yellowpages.superpages.com/listings.jsp?CS=L&MCBP=true&C=peanuts+deluxe+cafe%2C+san+jose+ca&STYPE=S&search=Find+It&submit=Search
#limit=
# http://www.superpages.com/bp/San-Jose-CA/Peanuts-Deluxe-Cafe-L0020274184.htm?C=peanuts+deluxe+cafe%2C+san+jose+ca&lbp=1&STYPE=S&TR=77&bidType=FLCLIK&PGID=yp609.8083.1405754605752.1951281190764&dls=true&bpp=1
#query="Peanuts-Deluxe-Cafe"
#location="San-Jose-CA"

class SuperPagesCrawlSpider(CrawlSpider):

	name = 'superpagesCrawlSpider'

	def __init__(self, location, state, query, *args, **kwargs):
		self.rules = (Rule(	LinkExtractor(allow=(r'/bp/'+location+'/'+query+'*')),
							callback='parse_item',
							follow = True),)
		super(SuperPagesCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['wwww.superpages.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://yellowpages.superpages.com/listings.jsp?CS=L&MCBP=true&C='+query+'%2C+'+location+'+'+state+'&STYPE=S&search=Find+It&submit=Search']

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="coreBizName_nonad"]/h1/text()')
		l.add_xpath('address','//*[@id="coreBizAddress"]/text()')
		l.add_xpath('phone','//*[@id="phNos"]/span/text()')
		l.add_value('websource', 'superpages')
		return  l.load_item()