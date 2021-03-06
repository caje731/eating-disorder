
import os, subprocess
from scrapy.command import ScrapyCommand

class AllCrawlCommand(ScrapyCommand):
	required_project = True
	
	def short_desc(self):
		return "Schedule a distributed run for all available spiders"
		
	def run(self, args, opts):
		crawler 	= self.crawler_process.create_crawler(self.crawler_process.settings)
		spider_names 	= crawler.spiders.list()
		for spider in spider_names:
			args.append('spider='+spider)
		subprocess.call(['python', os.getcwd() + "/distributer.py"] + args)

if __name__ == "__main__":
	print 	'Usage: scrapy allcrawl arg1=value1 arg2=value2 ...'
	print
	print	'This command is a custom command to be used from within the scanner project.'
	print	'It triggers crawl for all available spiders in the project. Argument examples:'
	print	'city="Mumbai" area="Pali Hill" location="Bandra West" query="Stomach" category="food" state="MH" pincode=""'
