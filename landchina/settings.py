# coding: utf-8
# Scrapy settings for landchina project

SPIDER_MODULES = ['landchina.spiders']
NEWSPIDER_MODULE = 'landchina.spiders'
DEFAULT_ITEM_CLASS = 'landchina.items.DealResult'

ITEM_PIPELINES = {'landchina.pipelines.SaveExcelPipeline': 1}


BASE_URL = u'http://www.landchina.com/default.aspx?tabid=263&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&p=9f2c3acd-0256-4da2-a659-6949c4671a2a%3A{start}~{end}%7C42ad98ae-c46a-40aa-aacc-c0884036eeaf%{province}'

PROVINCE_BASE = u'3A{value}%u2593%7E{key}'
PROVINCE_MAP = {
    u'北京市':   '11',
    u'天津市':   '12',
    u'河北省':   '13',
    u'山西省':   '14',
    u'内蒙古':   '15',
    u'辽宁省':   '21',
    u'吉林省':   '22',
    u'黑龙江省': '23',
    u'上海市':   '31',
    u'江苏省':   '32',
    u'浙江省':   '33',
    u'安徽省':   '34',
    u'福建省':   '35',
    u'江西省':   '36',
    u'山东省':   '37',
    u'河南省':   '41',
    u'湖北省':   '42',
    u'湖南省':   '43',
    u'广东省':   '44',
    u'广西壮族': '45',
    u'海南省':   '46',
    u'重庆市':   '50',
    u'四川省':   '51',
    u'贵州省':   '52',
    u'云南省':   '53',
    u'西藏':     '54',
    u'陕西省':   '61',
    u'甘肃省':   '62',
    u'青海省':   '63',
    u'宁夏回族': '64',
    u'新疆维吾尔': '65',
    u'新疆建设兵团': '66',
}

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