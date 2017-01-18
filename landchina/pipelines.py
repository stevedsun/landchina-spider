# coding: utf-8

import re
import os
import xlwt

XLSDIR = 'results'


class SaveExcelPipeline(object):

    def __init__(self):
        self.filenames = {}

    def save_to_file(self, filename, item):
        if filename not in self.filename:
            self.filenames[filename] = 0
            self.init_new_excel(filename)

        self.text_to_excel(filename, item)

    def init_new_excel(self, filename):
        xls = xlwt.Workbook()
        sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
        sheet.write(0, 0, u'行政区')
        sheet.write(0, 1, u'项目名称')
        sheet.write(0, 2, u'项目位置')
        sheet.write(0, 3, u'面积(公顷)')
        sheet.write(0, 4, u'土地来源')
        sheet.write(0, 5, u'土地用途')
        sheet.write(0, 6, u'供地方式')
        sheet.write(0, 7, u'土地使用年限')
        sheet.write(0, 8, u'行业分类')
        sheet.write(0, 9, u'土地级别')
        sheet.write(0, 10,u'成交价格(万元)')
        sheet.write(0, 11,u'土地使用权人')
        sheet.write(0, 12,u'下限')
        sheet.write(0, 13,u'上限')
        sheet.write(0, 14,u'约定交地时间')
        sheet.write(0, 15,u'约定开工时间')
        sheet.write(0, 16,u'约定竣工时间')
        sheet.write(0, 17,u'合同签订日期')
        xls.save(os.path.join(XLSDIR, filename + '.xls'))


    def process_item(self, item, spider):
        date = item['qy_time']
        r = re.compile(u'[0-9]\d*年[0-9]\d*月')
        date = re.search(r, date).group(0)
        filename = '-'.join([spider.where, date])
        self.save_to_file(filename, item)
        return item

    def text_to_excel(self, filename, item):
        self.filenames[filename] += 1
        self.sheet.write(self.filenames[filename], 0, item['domain'] )
        self.sheet.write(self.filenames[filename], 1, item['name']   )
        self.sheet.write(self.filenames[filename], 2, item['addr']   )
        self.sheet.write(self.filenames[filename], 3, item['size']   )
        self.sheet.write(self.filenames[filename], 4, item['src']    )
        self.sheet.write(self.filenames[filename], 5, item['use']    )
        self.sheet.write(self.filenames[filename], 6, item['method'] )
        self.sheet.write(self.filenames[filename], 7, item['util']   )
        self.sheet.write(self.filenames[filename], 8, item['catalog'])
        self.sheet.write(self.filenames[filename], 9, item['lv']     )
        self.sheet.write(self.filenames[filename], 10, item['price']  )
        self.sheet.write(self.filenames[filename], 11, item['user']   )
        self.sheet.write(self.filenames[filename], 12, item['cap_b']  )
        self.sheet.write(self.filenames[filename], 13, item['cap_h']  )
        self.sheet.write(self.filenames[filename], 14, item['jd_time'])
        self.sheet.write(self.filenames[filename], 15, item['kg_time'])
        self.sheet.write(self.filenames[filename], 16, item['jg_time'])
        self.sheet.write(self.filenames[filename], 17, item['qy_time'])
        self.xls.save(os.path.join(XLSDIR, filename + '.xls'))
