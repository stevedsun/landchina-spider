# coding: utf-8
import calendar
import datetime
import logging
import re
import time

from scrapy.http import Request
from scrapy.spiders import Spider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from landchina.items import DealResult
from landchina.settings import BASE_URL, PROVINCE_MAP, PROVINCE_BASE, CELL_MAP, WEB_DRIVER_PATH

log = logging.getLogger(__name__)


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
        log.info("** Finished page: {page}, cost: {cost} seconds **".format(
            time=datetime.datetime.now(),
            url=self.url,
            page=self.page_no,
            cost=now - self.get_last()
        ))

        self.set_last(now)


class Province(object):
    def __init__(self, name, lite_code, code, url_code):
        self.name = name
        self.lite_code = lite_code
        self.code = code
        self.url_code = url_code
        self.p_code = PROVINCE_BASE.format(key=self.url_code,
                                           value=self.code)


class Mapper(object):
    def __init__(self, driver, where, begin, end):
        self.driver = driver
        self.where = where
        self.begin = begin
        self.end = end
        self.province_handler = None
        self.curr = None

    def get_province(self):
        p_code, p_name = self.where, PROVINCE_MAP.get(self.where, None)
        if not p_code:
            log.info("** Province (%s) NOT FOUND !! **" % self.where)
            raise ValueError

        lite_code = p_code.strip().rstrip('0')
        log.info("::::::::::::::::::::::::: %s :::::::::::::::::::::::::" % p_name)
        url_code = u''
        for letter in p_name:
            url_code += '%%u%x' % ord(letter)

        self.province_handler = Province(p_name, lite_code, p_code, url_code)
        return self.prvn

    @property
    def prvn(self):
        if self.province_handler:
            return self.province_handler
        return self.get_province()

    def iterurl(self, prvn):
        start = datetime.datetime.strptime(self.begin, "%Y-%m").date()
        stop = datetime.datetime.strptime(self.end, "%Y-%m").date()
        curr = start
        while curr <= stop:
            month_last = calendar.monthrange(curr.year, curr.month)[1]
            self.curr = '{year}-{month}'.format(year=curr.year, month=curr.month)
            from_date = '{year}-{month}-{day}'.format(year=curr.year,
                                                      month=curr.month,
                                                      day=1)
            to_date = '{year}-{month}-{day}'.format(year=curr.year,
                                                    month=curr.month,
                                                    day=month_last)
            yield BASE_URL.format(province=prvn.lite_code,
                                  start=from_date,
                                  end=to_date)

            try:
                curr = curr.replace(month=curr.month + 1)
            except ValueError:
                curr = curr.replace(year=curr.year + 1, month=1)

    def itercellurl(self):
        for url in self.iterurl(self.prvn):
            page = Page(url, self.driver)
            while page:
                for cell_url in page.fetchall():
                    yield cell_url
                BreakPointTrack(url, page.page_no)
                page = page.go_to_next()

    def iterreq(self):
        for cellurl in self.itercellurl():
            request = Request(cellurl)
            request.meta['PhantomJS'] = True
            yield request


class Page(object):
    def __init__(self, url, driver, page_no=1, page_max=0):
        self.url = url
        self.page_max = page_max
        self.page_no = page_no
        self.driver = driver
        if self.page_no == 1:
            log.info("Downloading URL: %s ... " % self.url)
            self.driver.get(self.url)
        if self.page_max == 0:
            self.get_max_page()
        log.info("Fetching Page: %s ... " % page_no)

    def get_max_page(self):
        try:
            paper = self.driver.find_element_by_class_name('pager')
            self.page_max = int(re.search(r'[0-9]\d*', paper.text).group(0))
        except NoSuchElementException:
            self.page_max = 1

    def go_to_next(self):
        if self.page_no >= self.page_max:
            return None
        log.info("==> Skipping to Page: %s ... " % (self.page_no + 1))
        self.driver.execute_script(
            "document.getElementById('TAB_QuerySubmitPagerData').setAttribute('value', %s)" % (self.page_no + 1))
        self.driver.execute_script("document.getElementById('mainForm').submit()")
        return Page(self.url, self.driver, self.page_no + 1, self.page_max)

    def fetchall(self):
        try:
            items = self.driver.find_elements_by_css_selector('.queryCellBordy a')
        except NoSuchElementException:
            log.error("** TABLE NOT FOUND in url: %s **" % self.url)
            raise StopIteration

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
        where = kwargs.pop('where', None)
        begin = kwargs.pop('begin', None)
        end = kwargs.pop('end', None)
        if isinstance(where, str):
            where = where.decode('utf-8')

        service_args = ['--load-images=false', '--disk-cache=true']
        self.driver = webdriver.Chrome(WEB_DRIVER_PATH, service_args=service_args)
        self.driver.implicitly_wait(10)

        self.mapper = Mapper(self.driver, where, begin, end)
        self.prvn = self.mapper.prvn
        super(LandDealSpider, self).__init__(name, **kwargs)

    def close(self, reason):
        self.driver.quit()

    def start_requests(self):
        return self.mapper.iterreq()

    def parse(self, response):
        item = DealResult()

        value = response.css("#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl::text").extract()
        item['size'] = value[0] if value else u''
        for k, v in CELL_MAP.iteritems():
            value = response.css(v + "::text").extract()
            if k == 'src' and item.get('size', None):
                try:
                    item[k] = value[0] if value else u''
                    if item[k] == item['size']:
                        item[k] = u"现有建设用地"
                    elif float(item[k]) == 0:
                        item[k] = u"新增建设用地"
                    else:
                        item[k] = u"新增建设用地(来自存量库)"
                except:
                    item[k] = value[0] if value else u''
            else:
                item[k] = value[0] if value else u''
                if item[k] == u'1900-01-01':
                    item[k] = u' '

        # Update #001
        item['where_code'] = self.prvn.code
        item['where'] = self.prvn.name
        item['parent_code'] = ''.join([self.prvn.code[:2], "0000"])
        item['parent_where'] = PROVINCE_MAP.get(item['parent_code'], "?")

        return [item]
