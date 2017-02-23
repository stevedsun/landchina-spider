# coding: utf-8
import json
# Scrapy settings for landchina project
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 0.1
# AUTOTHROTTLE_MAX_DELAY = 600
COOKIES_ENABLES = False
SPIDER_MODULES = ['landchina.spiders']
NEWSPIDER_MODULE = 'landchina.spiders'
DEFAULT_ITEM_CLASS = 'landchina.items.DealResult'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'landchina.middlewares.randomua.RandomUserAgentMiddleware': 400
}

WEB_DRIVER_PATH = '/usr/local/bin/chromedriver'

ITEM_PIPELINES = {'landchina.pipelines.SaveExcelPipeline': 1}

BASE_URL = u'http://www.landchina.com/default.aspx?tabid=263&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&p=9f2c3acd' \
           u'-0256-4da2-a659-6949c4671a2a%3A{start}~{end}%7C42ad98ae-c46a-40aa-aacc-c0884036eeaf%{province} '

PROVINCE_BASE = u'3A{value}%u2593%7E{key}'

CELL_MAP = {
    'domain': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl',
    'name': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl',
    'addr': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl',
    # 'size': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl',
    'src': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl',
    'use': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl',
    'method': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl',
    'util': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl',
    'catalog': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl',
    'lv': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl',
    'price': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl',
    'user': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl',
    'cap_b': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl',
    'cap_h': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl',
    'jd_time': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl',
    'kg_time': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2_ctrl',
    'jg_time': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl',
    'qy_time': '#mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl'
}

with open('location.json', 'r') as f:
        PROVINCE_MAP = json.load(f)

RES_MAPPING = {
    u'行政区': 'domain',
    u'项目名称': 'name',
    u'项目位置': 'addr',
    u'面积(公顷)': 'size',
    u'土地来源': 'src',
    u'土地用途': 'use',
    u'供地方式': 'method',
    u'土地使用年限': 'util',
    u'行业分类': 'catalog',
    u'土地级别': 'lv',
    u'成交价格(万元)': 'price',
    u'土地使用权人': 'user',
    u'下限': 'cap_b',
    u'上限': 'cap_h',
    u'约定交地时间': 'jd_time',
    u'约定开工时间': 'kg_time',
    u'约定竣工时间': 'jg_time',
    u'合同签订日期': 'qy_time'
}
