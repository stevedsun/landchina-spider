# coding: utf-8

from scrapy.http import HtmlResponse
from selenium import webdriver


class PhantomJSMiddleware(object):
    def process_request(self, request, spider):
        if request.meta.has_key('PhantomJS'):
            service_args = ['--load-images=false', '--disk-cache=true']
            print 'PhantomJS Requesting: ', request.url
            try:
                driver = webdriver.PhantomJS(service_args=service_args)
                driver.get(request.url)
                content = driver.page_source.encode('utf-8')
                url = driver.current_url.encode('utf-8')
                driver.quit()
                if content == '<html><head></head><body></body></html>':
                    return HtmlResponse(request.url, encoding ='utf-8', status=503, body='')
                else:
                    return HtmlResponse(url, encoding='utf-8', status=200, body=content)

            except:
                return HtmlResponse(request.url, encoding='utf-8', status=503, body='')
        else:
            print 'Common Requesting: ', request.url
