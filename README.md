# landchina 数据爬虫

基于 scrapy 框架，使用 selenium + phantomJS 解析动态数据。

## 安装与执行

macOS/Linux 环境下，先下载对应平台的~~phantomJS~~ [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)，放在系统全局PATH目录下(如`/usr/local/bin`)。

安装 python2 及 pip， 执行：

```
pip install -r requirements.txt
./start.sh
```

数据保存在results文件内。

## ChangeLog

* 2017-01-18 增加伪造UA；修改日期格式，按月存储表单
* 2017-01-16 增加断点日志，完善中间件调用流程
* 2017-01-13 更新第一个可用版本


