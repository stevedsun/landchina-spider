# coding: utf-8
import datetime

from scrapy.spiders import Spider
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException

from landchina.items import DealResult
from landchina.settings import BASE_URL, PROVINCE_BASE, PROVINCE_MAP


class Province(object):

    def __init__(self, name, code, urlcode):
        self.name = name
        self.code = code
        self.urlcode = urlcode
        self.pcode = PROVINCE_BASE.format(key=self.urlcode,
                                         value=self.code)


class Mapper(object):

    def __init__(self, driver):
        self.driver = driver

    def iterprvn(self, prvns=None):
        if not prvns:
            pmap = PROVINCE_MAP
        else:
            pmap = prvns

        for pname, pcode in pmap.iteritems():
            urlcode = u''
            for letter in pname:
                urlcode += '%%u%x' % ord(letter)

            yield Province(pname, pcode, urlcode)


    def iterurl(self, prvn, begin='2009-1-1', end='2017-1-1'):
        start = datetime.datetime.strptime(begin, "%Y-%m-%d").date()
        stop = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        curr = start
        try:
            nxt = curr.replace(month=curr.month+1)
        except ValueError:
            nxt = curr.replace(year=curr.year+1, month=1)

        while nxt <= stop:
            yield BASE_URL.format(province=prvn.pcode,
                                  start=curr.isoformat(),
                                  end=nxt.isoformat())

            try:
                curr, nxt = nxt, nxt.replace(month=nxt.month+1)
            except ValueError:
                curr, nxt = nxt, nxt.replace(year=nxt.year+1, month=1)

    def itercellurl(self):
        for prvn in self.iterprvn():
            for url in self.iterurl(prvn):
                page = Page(url, self.driver)
                while page:
                    for cellurl in page.fetchall():
                        yield cellurl
                    page.go_to_next()

    def iterreq(self):
        for cellurl in self.itercellurl():
            yield Request(cellurl)


class Page(object):

    def __init__(self, url, driver, page_no=1):
        self.url = url
        self.page_no = page_no
        self.driver = driver
        if self.page_no == 1:
            self.driver.get(self.url)

        self.next_btn = self.get_next_btn()

    def go_to_next(self):
        if not self.next_btn:
            return None

        self.next_btn.click()
        new_page = Page(self.url, self.driver, self.page_no+1)
        return new_page

    def get_next_btn(self):
        try:
            btn = self.driver.find_element_by_link_text(u'下页')
            if btn.get_attribute('disabled'):
                return None
            return btn
        except NoSuchElementException:
            return None

    def fetchall(self):
        try:
            items = self.driver.find_elements_by_css_selector('.queryCellBordy a')
        except NoSuchElementException:
            yield None

        for item in items:
            url = item.get_attribute('href')
            if not url or 'tabid=386' not in url:
                continue
            else:
                yield url


class LandDealSpider(Spider):
    name = "landdeal"
    allowed_domains = ["landchina.com"]

    def __init__(self):
        self.driver = None
        super(LandDealSpider, self).__init__()

    def start_requests(self):
        mapper = Mapper(self.driver)
        return mapper.iterreq()

    def parse(self, response):
        item = DealResult()
        domain = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl::text').extract()
        name = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl::text').extract()
        addr = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl::text').extract()
        size = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl::text').extract()
        src = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl::text').extract()
        use = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl::text').extract()
        method = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl::text').extract()
        util = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl::text').extract()
        catalog = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl::text').extract()
        lv = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl::text').extract()
        price = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl::text').extract()
        user = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl::text').extract()
        cap_b = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl::text').extract()
        cap_h = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl::text').extract()
        jd_time = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl::text').extract()
        kg_time = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2_ctrl::text').extract()
        jg_time = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl::text').extract()
        qy_time = response.css('#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl::text').extract()

        item['domain'] = domain[0] if domain else u''
        item['name'] = name[0] if name else u''
        item['addr'] = addr[0] if addr else u''
        item['size'] = size[0] if size else u''
        item['src'] = src[0] if src else u''
        item['use'] = use[0] if use else u''
        item['method'] = method[0] if method else u''
        item['util'] = util[0] if util else u''
        item['catalog'] = catalog[0] if catalog else u''
        item['lv'] = lv[0] if lv else u''
        item['price'] = price[0] if price else u''
        item['user'] = user[0] if user else u''
        item['cap_b'] = cap_b[0] if cap_b else u''
        item['cap_h'] = cap_h[0] if cap_h else u''
        item['jd_time'] = jd_time[0] if jd_time else u''
        item['kg_time'] = kg_time[0] if kg_time else u''
        item['jg_time'] = jg_time[0] if jg_time else u''
        item['qy_time'] = qy_time[0] if qy_time else u''

        return [item]
