# coding: utf-8

import unittest
from landchina.spider import UrlMapper


class UrlMapperTestCase(unittest.TestCase):

    def setUp(self):
        self.obj = UrlMapper()

    def tearDown(self):
        self.obj = None

    def test_catch_page(self):
        prvns = {u'江苏省': '32'}
        start_time = '2009-1-1'
        end_time = '2009-2-1'
        for prvn in self.obj.iterprvn(prvns):
            for url in self.iterurl(prvn, start_time, end_time):
                self.assertEqual(url is not None, True)
