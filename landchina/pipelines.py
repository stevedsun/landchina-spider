# coding: utf-8

import re
import os
import xlwt

XLSDIR = 'results'


class SaveExcelPipeline(object):

    def __init__(self):
        # {filename: index in handlers}
        self.filenames = {}
        self.handlers = []

    def gc_old_xls(self):
        if len(self.filenames) > 3:
            del self.handler[0]
            self.handler = self.handler[1:]

    def save_to_file(self, filename, item):
        if filename not in self.filenames:
            self.init_new_excel(filename)
            self.gc_old_xls()

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
        self.handlers.append(xls)
        self.filenames[filename] = len(self.handlers) - 1


    def process_item(self, item, spider):
        date = item['qy_time']
        r = re.compile(u'[0-9]\d*年[0-9]\d*月')
        date = re.search(r, date).group(0)
        filename = '-'.join([spider.where, date])
        self.save_to_file(filename, item)
        return item

    def text_to_excel(self, filename, item):
        index = self.filenames[filename]
        xls = self.handlers[index]
        sheet = xls.get_sheet('sheet1')
        row = sheet.last_used_row + 1
        sheet.write(row, 0, item['domain'] )
        sheet.write(row, 1, item['name']   )
        sheet.write(row, 2, item['addr']   )
        sheet.write(row, 3, item['size']   )
        sheet.write(row, 4, item['src']    )
        sheet.write(row, 5, item['use']    )
        sheet.write(row, 6, item['method'] )
        sheet.write(row, 7, item['util']   )
        sheet.write(row, 8, item['catalog'])
        sheet.write(row, 9, item['lv']     )
        sheet.write(row, 10, item['price']  )
        sheet.write(row, 11, item['user']   )
        sheet.write(row, 12, item['cap_b']  )
        sheet.write(row, 13, item['cap_h']  )
        sheet.write(row, 14, item['jd_time'])
        sheet.write(row, 15, item['kg_time'])
        sheet.write(row, 16, item['jg_time'])
        sheet.write(row, 17, item['qy_time'])
        xls.save(os.path.join(XLSDIR, filename + '.xls'))
