import scrapy
from scrapy.http import FormRequest
from proxy_parser.items import ProxyItem


class ProxySpider(scrapy.Spider):
    name = 'proxy_spider'

    start_urls = ['http://spys.one/proxies/']

    def parse(self, response):
        token = response.xpath('//input[@name="xf0"]/@value').extract_first()

        yield FormRequest(url=response.url,
                          formdata={'xf0': token,
                                    'xpp': '5',
                                    'xf1': '0',
                                    'xf2': '0',
                                    'xf4': '0',
                                    'xf5': '0'
                                    },
                          callback=self.parse_proxy_list)

    def parse_proxy_list(self, response):
        js = response.xpath('/html/body/script/text()').extract_first()
        js_context = get_js_vars(js)

        proxies = response.xpath('//tr[@onmouseover]/td[1]/font[2]')
        for proxy in proxies:
            item = ProxyItem()
            port_encoded = proxy.xpath('./script/text()').re_first(
                r'(?<=font>\"\+).+(?=\))')

            item['ip_address'] = proxy.xpath('.//text()').extract_first()
            item['port'] = get_port(port_encoded, js_context)
            yield item


def get_js_vars(source):
    local_context = {}
    exec(source, {'__builtins__': None}, local_context)
    return local_context


def get_port(source, context):
    source = 'result = (' + source.replace('+', ',') + ')'
    exec(source, {'__builtins__': None}, context)
    return ''.join(map(str, context['result']))
