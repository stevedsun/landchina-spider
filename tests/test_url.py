# coding: utf-8

import unittest
from landchina.spiders.deal import Mapper
from scrapy.http import Request


class UrlMapperTestCase(unittest.TestCase):

    def setUp(self):
        self.obj = Mapper()

    def tearDown(self):
        self.obj = None

    def test_url_map(self):
        prvns = {u'江苏省': '32'}
        start_time = '2009-1-1'
        end_time = '2009-3-1'
        for prvn in self.obj.iterprvn(prvns):
            for url in self.obj.iter_url(prvn, start_time, end_time):
                self.assertEqual(url is not None, True)

    def test_req_map(self):
        prvns = {u'江苏省': '32'}
        start_time = '2009-1-1'
        end_time = '2009-3-1'
        for prvn in self.obj.iterprvn(prvns):
            for url in self.obj.iter_url(prvn, start_time, end_time):
                req = Request(url)
                self.assertEqual(isinstance(req, Request), True)

    def test_cell_url_map(self):
        for url in self.obj.iter_cell_url():
            print url
