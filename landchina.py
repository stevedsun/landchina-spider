#!/usr/bin/env python
# coding=utf-8
import csv
import sys
import time
import calendar
import datetime
from selenium import webdriver

MONTH_FROM = "2016-4"
MONTH_TO = "2017-4"
PROVINCE = u"广东省".encode("utf-8")


def deal(date_from, date_to):
    filename = "./results/landchina/{0}_{1}~{2}".format(
        PROVINCE, date_from, date_to) + ".csv"
    print filename

    reload(sys)
    sys.setdefaultencoding("utf-8")

    browser = webdriver.Chrome()

    url = "http://www.landchina.com/default.aspx?tabid=263"
    browser.get(url)

    date_checkbox = browser.find_element_by_xpath(
        ".//*[@id='TAB_QueryConditionItem270']")
    date_checkbox.click()

    date_from_input = browser.find_element_by_xpath(
        ".//*[@id='TAB_queryDateItem_270_1']")
    date_from_input.send_keys(date_from)
    date_to_input = browser.find_element_by_xpath(
        ".//*[@id='TAB_queryDateItem_270_2']")
    date_to_input.send_keys(date_to)

    location_checkbox = browser.find_element_by_xpath(
        ".//*[@id='TAB_QueryConditionItem256']")
    location_checkbox.click()
    location_input = browser.find_element_by_xpath(
        ".//*[@id='TAB_queryTblEnumItem_256']")
    location_input.click()

    time.sleep(2)
    browser.switch_to_window(browser.window_handles[1])
    province_list = browser.find_elements_by_xpath(
        ".//*[@id='treeDemo_1_ul']/li")
    for province_tmp in province_list:
        if province_tmp.find_element_by_xpath(
                ".//a").get_attribute("title") in PROVINCE:
            province_tmp.find_element_by_xpath(".//a").click()
            break
    confirm_button = browser.find_element_by_xpath(
        ".//*[@id='Table1']/tbody/tr[1]/td/table/tbody/tr/td[3]/input[1]")
    confirm_button.click()
    time.sleep(2)
    browser.switch_to_window(browser.window_handles[0])

    query_button = browser.find_element_by_xpath(
        ".//*[@id='TAB_QueryButtonControl']")
    query_button.click()

    total_number_text = browser.find_element_by_xpath(
        ".//*[@id='mainModuleContainer_485_1113_1539_tdExtendProContainer']\
        /table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td[1]\
        ").text
    print "total_number: " + total_number_text
    if u"当前只显示200页".encode("utf-8") in total_number_text:
        print total_number_text
        print u"当前页数太多，请重新选择日期。"
        sys.exit()

    fieldnames = [
        u"行政区".encode("utf-8"),
        u"电子监管号".encode("Utf-8"),
        u"项目名称".encode("utf-8"),
        u"项目位置".encode("utf-8"),
        u"面积(公顷)".encode("utf-8"),
        u"土地来源".encode("utf-8"),
        u"土地用途".encode('utf-8'),
        u"供地方式".encode("utf-8"),
        u"土地使用年限".encode("utf-8"),
        u"行业分类".encode("utf-8"),
        u"土地级别".encode("utf-8"),
        u"成交价格(万元)".encode("utf-8"),
        u"分期支付约定".encode("utf-8"),
        u"土地使用权人".encode("utf-8"),
        u"约定容积率下限".encode("utf-8"),
        u"约定容积率上限".encode("utf-8"),
        u"约定交地时间".encode("utf-8"),
        u"约定开工时间".encode('utf-8'),
        u"约定竣工时间".encode("utf-8"),
        u"实际开工时间".encode("utf-8"),
        u"实际竣工时间".encode("utf-8"),
        u"批准单位".encode("utf-8"),
        u"合同签订日期".encode("utf-8"),
    ]

    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writerow({k: k for k in fieldnames})

    # 用于有时候下一页失效的时候
    # time.sleep(2)
    # goto_page_input = browser.find_element_by_xpath(
    #     ".//*[@id='mainModuleContainer_485_1113_1539_tdExtendProContainer']/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/input[1]")
    # goto_page_input.clear()
    # goto_page_input.send_keys("78")
    # go_buttion = browser.find_element_by_xpath(
    #     ".//*[@id='mainModuleContainer_485_1113_1539_tdExtendProContainer']/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/input[2]")
    # go_buttion.click()

    while True:
        tr_list = browser.find_elements_by_xpath(
            ".//*[@id='TAB_contentTable']/tbody/tr")[1:]
        tr_sum = len(tr_list)
        tr_num = 0
        while tr_num < tr_sum:
            # print('''window.open(" %s ", "_blank");''' %
            #       (tr_list[tr_num].find_element_by_xpath(".//td[3]/a")
            #        .get_attribute("href")))
            browser.execute_script(
                '''window.open("%s", "_blank");''' %
                (tr_list[tr_num].find_element_by_xpath(".//td[3]/a")
                 .get_attribute("href")))
            browser.switch_to_window(browser.window_handles[1])
#        time.sleep(1)
            td_list = browser.find_elements_by_xpath(
                ".//*[@id='mainModuleContainer_1855_1855']/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/div/table/tbody/tr/td")[5:]
            td_sum = len(td_list)
            td_num = 0
            mydict = {}
            while td_num + 1 < td_sum:
                key = td_list[td_num].text[:-1].encode("utf-8")
                if key in "土地使用权人".encode("utf-8"):
                    td_num = td_num + 1
                value = td_list[td_num + 1].text.encode("utf-8")
#            print key + " " + value
                td_num = td_num + 2
                if key in "约定容积率".encode("utf-8"):
                    limit = value.split(u"下限:")[1].split(u"上限:")
                    mydict["约定容积率下限".encode("utf-8")] = limit[0]
                    mydict["约定容积率上限".encode("utf-8")] = limit[1]
                    continue
                mydict[key] = value

            with open(filename, "a") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writerow(
                    {k: v for k, v in mydict.items() if k in fieldnames})

            browser.close()
            browser.switch_to_window(browser.window_handles[0])
            tr_num = tr_num + 1

        page_list = browser.find_elements_by_xpath(
            ".//*[@id='mainModuleContainer_485_1113_1539_tdExtendProContainer']/table/tbody/tr[1]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/a")
        if not page_list:
            break
        next_page = page_list[-2]
        if next_page.get_attribute("disabled") is not None:
            break
        print next_page.get_attribute("onclick")
        next_page.click()
        time.sleep(2)

    browser.close()


if __name__ == "__main__":
    start = datetime.datetime.strptime(MONTH_FROM, "%Y-%m").date()
    stop = datetime.datetime.strptime(MONTH_TO, "%Y-%m").date()
    current = start
    while current <= stop:
        month_lastday = calendar.monthrange(current.year,
                                            current.month)[1]
        date_from = "{year}-{month}-{day}".format(year=current.year,
                                                  month=current.month,
                                                  day=1)
        date_to = "{year}-{month}-{day}".format(year=current.year,
                                                month=current.month,
                                                day=month_lastday)
        print date_from + "~" + date_to
        deal(date_from, date_to)
        try:
            current = current.replace(month=current.month + 1)
        except ValueError:
            current = current.replace(year=current.year + 1, month=1)
