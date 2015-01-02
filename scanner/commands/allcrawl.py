import os, subprocess
from scrapy.command import ScrapyCommand

class AllCrawlCommand(ScrapyCommand):
	required_project = True
	
	def short_desc(self):
		return "Schedule a run for all available spiders"
		
	def run(self, args, opts):
		crawler 		= self.crawler_process.create_crawler(self.crawler_process.settings)
		spider_names 	= crawler.spiders.list()
		for spider in spider_names:
			args.append('spider='+spider)
		#dist_response = os.system('python "C:\Git Repos\MassBlurb\scanner\util\distribute.py" '+ ' '.join(args))
		subprocess.call(['python', "C:\GitRepos\MassBlurb\scanner\util\distribute.py"] + args)
		
		#subprocess.check_output('python "C:\Git Repos\MassBlurb\scanner\util\distribute.py" ' + ' '.join(args), shell=True)

if __name__ == "__main__":
	print 	'Usage: scrapy allcrawl arg1=value1 arg2=value2 ...'
	print
	print	'This command is a custom command to be used from within the scanner project.'
	print	'It triggers crawl for all available spiders in the project. Argument examples:'
	print	'city="Mumbai" area="Pali Hill" location="Bandra West" query="Stomach" category="food" state="MH" pincode=""'
