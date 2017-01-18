# coding: utf-8

import os
import xlwt

XLSDIR = 'results'


class SaveExcelPipeline(object):

    def __init__(self):
        self.xls, self.sheet, self.filename, self.row = None, None, None, None

    def save_to_file(self, filename, item):
        if filename != self.filename:
            self.filename = filename
            self.row = 0
            self.init_new_excel()

        self.text_to_excel(item)

    def init_new_excel(self):
        self.xls = xlwt.Workbook()
        self.sheet = self.xls.add_sheet('sheet1', cell_overwrite_ok=True)
        self.sheet.write(self.row, 0, u'行政区')
        self.sheet.write(self.row, 1, u'项目名称')
        self.sheet.write(self.row, 2, u'项目位置')
        self.sheet.write(self.row, 3, u'面积(公顷)')
        self.sheet.write(self.row, 4, u'土地来源')
        self.sheet.write(self.row, 5, u'土地用途')
        self.sheet.write(self.row, 6, u'供地方式')
        self.sheet.write(self.row, 7, u'土地使用年限')
        self.sheet.write(self.row, 8, u'行业分类')
        self.sheet.write(self.row, 9, u'土地级别')
        self.sheet.write(self.row, 10,u'成交价格(万元)')
        self.sheet.write(self.row, 11,u'土地使用权人')
        self.sheet.write(self.row, 12,u'下限')
        self.sheet.write(self.row, 13,u'上限')
        self.sheet.write(self.row, 14,u'约定交地时间')
        self.sheet.write(self.row, 15,u'约定开工时间')
        self.sheet.write(self.row, 16,u'约定竣工时间')
        self.sheet.write(self.row, 17,u'合同签订日期')
        self.xls.save(os.path.join(XLSDIR, self.filename + '.xls'))

    def process_item(self, item, spider):
        filename = '-'.join([spider.where, spider.mapper.curr, spider.mapper.nxt])
        self.save_to_file(filename, item)
        return item

    def text_to_excel(self, item):
        self.row += 1
        self.sheet.write(self.row, 0, item['domain'] )
        self.sheet.write(self.row, 1, item['name']   )
        self.sheet.write(self.row, 2, item['addr']   )
        self.sheet.write(self.row, 3, item['size']   )
        self.sheet.write(self.row, 4, item['src']    )
        self.sheet.write(self.row, 5, item['use']    )
        self.sheet.write(self.row, 6, item['method'] )
        self.sheet.write(self.row, 7, item['util']   )
        self.sheet.write(self.row, 8, item['catalog'])
        self.sheet.write(self.row, 9, item['lv']     )
        self.sheet.write(self.row, 10, item['price']  )
        self.sheet.write(self.row, 11, item['user']   )
        self.sheet.write(self.row, 12, item['cap_b']  )
        self.sheet.write(self.row, 13, item['cap_h']  )
        self.sheet.write(self.row, 14, item['jd_time'])
        self.sheet.write(self.row, 15, item['kg_time'])
        self.sheet.write(self.row, 16, item['jg_time'])
        self.sheet.write(self.row, 17, item['qy_time'])
        self.xls.save(os.path.join(XLSDIR, self.filename + '.xls'))
