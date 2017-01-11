# coding: utf-8
import datetime

from scrapy.spiders import Spider
from scrapy.selector import Selector

from landchina.items import DealResult
from landchina.settings import BASE_URL, PROVINCE_BASE, PROVINCE_MAP, RES_MAPPING


class Province(object):
    def __init__(self, name, code, urlcode):
        self.name = name
        self.code = code
        self.urlcode = urlcode


class UrlMapper(object):
    def __init__(self):
        pass

    def iterprvn(self, prvns=None):
        if not prvns:
            pmap = PROVINCE_MAP
        else:
            pmap = prvns

        for pname, pcode in pmap.iteritems():
            print '='*10 + '%s' % pname + '='*10
            urlcode = u''
            for letter in pname:
                urlcode += '%%u%x' % ord(letter)

            yield Province(pname, pcode, urlcode)


    def iterurl(self, prvn, begin, end):
        start = datetime.datetime.strptime(begin, "%Y-%m-%d").date()
        stop = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        curr = start
        try:
            nxt = curr.replace(month=curr.month+1)
        except ValueError:
            nxt = curr.replace(year=curr.year+1, month=1)

        while nxt < stop:
            yield BASE_URL.format(province=prvn.urlcode,
                                  start=curr.isoformat(),
                                  end=nxt.isoformat())

            try:
                curr, nxt = nxt, nxt.replace(month=nxt.month+1)
            except ValueError:
                curr, nxt = nxt, nxt.replace(year=nxt.year+1, month=1)



class LandDealSpider(Spider):
    name = "landdeal"
    allowed_domains = ["landchina.com"]
#     start_urls = [
        # "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
#     ]

    def start_requests(self):
        pass


    def parse(self, response):
        sites = response.css('#site-list-content > div.site-item > div.title-and-desc')
        items = []

        for site in sites:
            item = DealResult()
            item['name'] = site.css(
                'a > div.site-title::text').extract_first().strip()
            item['url'] = site.xpath(
                'a/@href').extract_first().strip()
            item['description'] = site.css(
                'div.site-descr::text').extract_first().strip()
            items.append(item)

        return items
