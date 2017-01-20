# coding: utf-8

import ConfigParser
import os

def main():
    code, begin, end = None, None, None
    try:
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read('info.ini')
        code = config.get('config', 'code')
        begin = config.get('config', 'begin')
        end = config.get('config', 'end')
    except Exception as e:
        print 'Error while load config file.', e.message

    if code and begin and end:
        os.system('scrapy crawl -a where={code} -a begin={begin} -a end={end} -L INFO landdeal'.format(
            code=code,
            begin=begin,
            end=end
        ))


if __name__ == "__main__":
    main()
