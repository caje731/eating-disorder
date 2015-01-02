from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors import LinkExtractor

from scanner.items import BusinessInfoItem

#DONE. But results are not complete. Recheck.
#AllProducts
#start_url="http://www.allproducts.com/search2/search.php?query=Lightvision+technologies&kind=supplier&Search.x=0&Search.y=0"
#category="light"
#query="lightvision"


class AllProductsCrawlSpider(CrawlSpider):

	name = 'allproductsCrawlSpider'

	def __init__(self, category, query, *args, **kwargs):
		q = str(query.split()[0])
		self.rules = 	(	Rule(LinkExtractor(allow=(r'/'+category+'/'+q),deny=(r'/'+category+'/'+q+'/\d+',r'/'+category+'/'+q+'/showroom*')),
								callback='parse_item',
								follow = True),
						)
		self.allowed_domains = ['www.allproducts.com']
		if 'start_url' in kwargs:
			self.start_urls = [kwargs.get('start_url')]
		else:
			self.start_urls = ['http://www.allproducts.com/search2/search.php?query='+q+'&kind=supplier&Search.x=0&Search.y=0']
		super(AllProductsCrawlSpider, self).__init__(*args, **kwargs)

	def parse_item(self,response):

		l = ItemLoader(item = BusinessInfoItem(),response = response)
		l.add_xpath('name','//*[@id="main"]/div[3]/div/strong/text()')
		l.add_xpath('address','//*[@id="main"]/div[2]/div[2]/div[3]/span[2]/text()')
		l.add_xpath('phone','//*[@id="main"]/div[2]/div[2]/div[4]/span[2]/text()')
		l.add_value('websource', 'allproducts')
		#l.add_xpath('sales_contact','//*[@id="main"]/div[2]/div[2]/div[2]/span[2]/text()')
		#l.add_xpath('company_profile','//*[@id="aupd"]/tbody/tr/td/div/p/text()')
		#l.add_xpath('year_of_establishment','//*[@id="main"]/div[2]/div[1]/div[2]/span[2]/text()')
		#l.add_xpath('capital','//*[@id="main"]/div[2]/div[1]/div[3]/span[2]/text()')
		#l.add_xpath('annual_sales','//*[@id="main"]/div[2]/div[1]/div[4]/span[2]/text()')
		#l.add_xpath('markets','//*[@id="main"]/div[2]/div[1]/div[7]/span[2]/ul/li[1]/text()')
		#l.add_xpath('url','//*[@id="main"]/div[2]/div[2]/div[7]/span[2]/a[1]/text()')
		#l.add_xpath('email','//*[@id="main"]/div[2]/div[2]/div[6]/span[2]/a/text()')

		return l.load_item()