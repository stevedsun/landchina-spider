# coding: utf-8
import datetime

from selenium import webdriver
from scrapy.spiders import Spider
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException

from landchina.items import DealResult
from landchina.settings import BASE_URL, PROVINCE_BASE, PROVINCE_MAP, CELL_MAP


class BreakPointTrack(object):

    def __init__(self, url, page_no):
        self.url = url
        self.page_no = page_no
        self.save()

    def save(self):
        track = "{time} - [url:{url}] - [page:{page}]\n".format(
            time=datetime.datetime.now(),
            url=self.url,
            page=self.page_no,
        )
        with open("breakpoint.log", "a") as f:
            f.write(track)


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
                page_ok = True
                while page and page_ok:
                    BreakPointTrack(url, page.page_no)
                    for cellurl in page.fetchall():
                        if not cellurl:
                            page_ok = False
                            break
                        yield cellurl
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

    def __init__(self, name=None, **kwargs):
        service_args = ['--load-images=false', '--disk-cache=true']
        self.driver = webdriver.PhantomJS(service_args=service_args)
        super(LandDealSpider, self).__init__(name, **kwargs)

    def close(self, reason):
        self.driver.quit()

    def start_requests(self):
        mapper = Mapper(self.driver)
        return mapper.iterreq()

    def parse(self, response):
        item = DealResult()

        for k, v in CELL_MAP.iteritems():
            value = response.css(v + "::text").extract()
            item[k] = value[0] if value else ''

        return [item]
