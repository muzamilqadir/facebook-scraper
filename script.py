import os
print os.popen("pip install -r requirements.txt").read()
print os.popen("scrapy crawl facebookspider --nolog -o data.csv -t csv").read()
