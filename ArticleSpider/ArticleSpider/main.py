from scrapy.cmdline import execute
import sys
import os

sys.path.append(__file__)

execute(['scrapy', 'crawl', 'jobbole'])
