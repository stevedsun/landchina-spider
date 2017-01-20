# coding: utf-8

import ConfigParser
import os

def main():
    try:
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read('info.ini')
        code = config['code']
        begin = config['begin']
        end = config['end']
    except:
        print 'Error parameter in info.ini'

    if code and begin and end:
        os.system('scrapy crawl -a where={code} -a begin={begin} -a end={end} -L INFO landdeal'.format(
            code=code,
            begin=begin,
            end=end
        ))


if __name__ == "__main__":
    main()
