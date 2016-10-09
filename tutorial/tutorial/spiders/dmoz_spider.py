import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["xueqiu.com"]
    start_urls = [
        "https://xueqiu.com/friendships/groups/members.json?page=1&uid=7315353232/",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)