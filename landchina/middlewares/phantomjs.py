# coding: utf-8

from scrapy.http import HtmlResponse
from selenium import webdriver
from fake_useragent import UserAgent


class PhantomJSMiddleware(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS(service_args=['--load-images=false', '--disk-cache=true'])

    def __del__(self):
        self.driver.quit()

    def process_request(self, request, spider):
        if request.meta.has_key('PhantomJS'):
            print 'PhantomJS Requesting: ', request.url
            ua = None
            try:
                ua = UserAgent().random
            except:
                ua = 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'

            request.headers.setdefault('User-Agent', ua)

            try:
                self.driver.get(request.url)
                content = self.driver.page_source.encode('utf-8')
                url = self.driver.current_url.encode('utf-8')
            except:
                return HtmlResponse(request.url, encoding='utf-8', status=503, body='')

            if content == '<html><head></head><body></body></html>':
                return HtmlResponse(request.url, encoding ='utf-8', status=503, body='')
            else:
                return HtmlResponse(url, encoding='utf-8', status=200, body=content)

        else:
            print 'Common Requesting: ', request.url
