import scrapy
from scrapy import Field


class ProxyItem(scrapy.Item):
    ip_address = Field()
    port = Field()
