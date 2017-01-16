# coding: utf-8

from scrapy.http import HtmlResponse
from selenium import webdriver


class PhantomJSMiddleware(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS(service_args=['--load-images=false', '--disk-cache=true'])

    def __del__(self):
        self.driver.quit()

    def process_request(self, request, spider):
        if request.meta.has_key('PhantomJS'):
            print 'PhantomJS Requesting: ', request.url
            try:
                self.driver.get(request.url)
                content = self.driver.page_source.encode('utf-8')
                url = self.driver.current_url.encode('utf-8')
                if content == '<html><head></head><body></body></html>':
                    return HtmlResponse(request.url, encoding ='utf-8', status=503, body='')
                else:
                    return HtmlResponse(url, encoding='utf-8', status=200, body=content)

            except:
                return HtmlResponse(request.url, encoding='utf-8', status=503, body='')
        else:
            print 'Common Requesting: ', request.url
