# coding: utf-8

import ConfigParser
import os

def main():
    config = ConfigParser.RawConfigParser()
    config.read('info.ini')
    code = config.get('code')
    begin = config.get('begin')
    end = config.get('end')

    if code and begin and end:
        os.system('scrapy crawl -a where={code} -a begin={begin} -a end={end} -L INFO landdeal'.format(
            code=code,
            begin=begin,
            end=end
        ))
    else:
        print 'Error parameter in info.ini'


if __name__ == "__main__":
    main()
