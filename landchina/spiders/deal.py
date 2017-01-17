# coding: utf-8
import datetime
import time
import re

from selenium import webdriver
from scrapy.spiders import Spider
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException

from landchina.items import DealResult
from landchina.settings import BASE_URL, PROVINCE_BASE, PROVINCE_MAP, CELL_MAP


class BreakPointTrack(object):
    last_time = time.time()

    def __init__(self, url, page_no):
        self.url = url
        self.page_no = page_no
        self.save()

    @classmethod
    def get_last(cls):
        return cls.last_time

    @classmethod
    def set_last(cls, now):
        cls.last_time = now

    def save(self):
        now = time.time()
        track = "{time} - [url:{url}] - [page:{page}] - [cost:{cost}]\n".format(
            time=datetime.datetime.now(),
            url=self.url,
            page=self.page_no,
            cost= now - self.get_last()
        )
        with open("breakpoint.log", "a") as f:
            f.write(track)

        self.set_last(now)

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
                    BreakPointTrack(url, page.page_no)
                    page = page.go_to_next()

    def iterreq(self):
        for cellurl in self.itercellurl():
            request = Request(cellurl)
            request.meta['PhantomJS'] = True
            yield request


class Page(object):

    def __init__(self, url, driver, page_no=1):
        self.url = url
        self.page_no = page_no
        self.driver = driver
        if self.page_no == 1:
            self.driver.get(self.url)
        paper = self.driver.find_element_by_class_name('pager')
        self.page_max = int(re.search(r'[0-9]\d*', paper.text).group(0))

    def go_to_next(self):
        if self.page_no >= self.page_max:
            return None
        self.driver.execute_script("document.getElementById('TAB_QuerySubmitPagerData').setAttribute('value', %s)" % (self.page_no+1))
        self.driver.execute_script("document.getElementById('mainForm').submit()")
        return Page(self.url, self.driver, self.page_no+1)

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

    def __init__(self, name=None, **kwargs):
        service_args = ['--load-images=false', '--disk-cache=true']
        self.driver = webdriver.PhantomJS(service_args=service_args)
        self.driver.implicitly_wait(10)
        super(LandDealSpider, self).__init__(name, **kwargs)

    def close(self, reason):
        self.driver.quit()

    def start_requests(self):
        mapper = Mapper(self.driver)
        return mapper.iterreq()

    def parse(self, response):
        item = DealResult()

        value = response.css("#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl::text").extract()
        item['size'] = value[0] if value else u''
        for k, v in CELL_MAP.iteritems():
            value = response.css(v + "::text").extract()
            if k == 'src' and item.get('size', None):
                item[k] = value[0] if value else u''
                if item[k] == item['size']:
                    item[k] = u"现有建设用地"
                elif float(item[k]) == 0:
                    item[k] = u"新增建设用地"
                else:
                    item[k] = u"新增建设用地(来自存量库)"
            else:
                item[k] = value[0] if value else u''
                if item[k] == u'1900-01-01':
                    item[k] = u' '

        return [item]
