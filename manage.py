# coding: utf-8

import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('code', nargs='?', default='320100', help='Province code')
    parser.add_argument('begin', nargs='?', default='2009-1', help='When to begin')
    parser.add_argument('end', nargs='?', default='2016-12', help='When to end')
    args = parser.parse_args()

    if args.code and args.begin and args.end:
        os.system('scrapy crawl -a where={code} -a begin={begin} -a end={end} -L INFO landdeal'.format(
            code=args.code,
            begin=args.begin,
            end=args.end
        ))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

