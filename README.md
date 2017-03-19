# landchina 数据爬虫

基于 scrapy 框架，使用 selenium + chromeDriver 解析动态数据。

## 快速使用
macOS/Linux 环境下，先下载对应平台的~~phantomJS~~ [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)，放在系统全局PATH目录下(如`/usr/local/bin`)。

安装 python2 及 pip， 执行：

```
pip install -r requirements.txt
python manage.py
```

数据保存在results文件内。

## 配置

想要更改爬取的行政区，需要在info.ini里填写对应的行政区编码(可在`location.json`文件里找到)，查询的起止时间。


## ChangeLog

* 2017-01-18 增加伪造UA；修改日期格式，按月存储表单
* 2017-01-16 增加断点日志，完善中间件调用流程
* 2017-01-13 更新第一个可用版本


