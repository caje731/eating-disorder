from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#JustDial India
#start_url="http://www.justdial.com/Mumbai/pop-tates"
#city="Mumbai"   ---> name --> Initials Capital
#query="Pop-Tates"  ---> business_name --> Initials Capital. MUST.
#locality=""


class JustDialIndiaCrawlSpider(CrawlSpider):

	name = 'justdialindiaCrawlSpider'

	def __init__(self, city, query, location, *args, **kwargs):
		
		city = city.replace(' ','-')
		query = query.replace(' ','-')
		location_1 	= location.split(' ')[0]
		location 	= location.replace(' ','-')
		
		self.rules = (Rule(	LinkExtractor(	allow=(	'/'+city+'/'+query+'.*'+location+'.*',
													'/'+city.capitalize()+'/'+query.capitalize()+'.*'+location_1.capitalize()+'.*'),
											deny=(	'/menu-order',
													'.*/\d$',
													'/?tab=menu',
													'/?tab=moreinfo',
													'tab=map',
													'/writereview')), 
							callback='parse_item',
							follow = True),)
		super(JustDialIndiaCrawlSpider, self).__init__(*args, **kwargs)
		self.allowed_domains = ['www.justdial.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.justdial.com/'+city+'/'+query+'-<near>-'+location]

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		
		l.add_xpath('name',		'/html/body/section[1]/section[2]/div/section/section[1]/aside/h1/span/span/text()')
		#l.add_xpath('address',	'/html/body/section[1]/section[2]/div/section/section[2]/section[2]/section[1]/aside/p[2]/span[2]/span/text()')
		l.add_xpath('address',  '//aside[@class="continfo "]/p[1]/span[2]/text()')
		#l.add_xpath('phone',	'/html/body/section[1]/section[2]/div/section/section[2]/section[2]/section[1]/aside/p[1]/span[2]/a/text()')
		l.add_xpath('phone',  	'//aside[@class="continfo "]/p[2]/a/text()')
		l.add_xpath('phone',  	'//aside[@class="continfo "]/p[3]/a/text()')
		l.add_xpath('timings', 	'//tr[@class="reset"]/td/text()')
		l.add_value('websource','justdialindia')
		return l.load_item()