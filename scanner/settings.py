# -*- coding: utf-8 -*-

# Scrapy settings for scanner project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scanner'

SPIDER_MODULES		= ['scanner.spiders']
NEWSPIDER_MODULE 	= 'scanner.spiders'
COMMANDS_MODULE 	= 'scanner.commands'
WEBSERVICE_RESOURCES = {
    'scrapy.contrib.webservice.crawler.CrawlerResource': 1,
    'scrapy.contrib.webservice.enginestatus.EngineStatusResource': 1,
    'scrapy.contrib.webservice.stats.StatsResource': 1,
	}
EXTENSIONS = {
    'scrapy.contrib.corestats.CoreStats': 0,
    'scrapy.webservice.WebService': 0,
    'scrapy.telnet.TelnetConsole': 0,
    'scrapy.contrib.memusage.MemoryUsage': 0,
    'scrapy.contrib.memdebug.MemoryDebugger': 0,
    'scrapy.contrib.closespider.CloseSpider': 0,
    'scrapy.contrib.feedexport.FeedExporter': 0,
    'scrapy.contrib.logstats.LogStats': 0,
    'scrapy.contrib.spiderstate.SpiderState': 0,
    'scrapy.contrib.throttle.AutoThrottle': 0,
}
WEBSERVICE_ENABLED = False
WEBSERVICE_PORT = 6655

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scanner (+http://www.yourdomain.com)'

