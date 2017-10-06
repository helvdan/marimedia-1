from file_client import FileClient
from marimedia import MarimediaRuDescriptor
from dateparser import parse
import argparse
import requests

class Crawler(object):

    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.file_client = FileClient()

    def crawl(self, stop_dated):
        print('starting to crawl')
        crawled_dict = {}
        for url in self.descriptor.newsline:
            print('navigating to url %s' % url)

            page_source_code = requests.get(url).text
            for item in self.descriptor.newsline.parse(page_source_code):
                print(item.pubdate)
                if stop_dated > item.pubdate:
                    self.file_client.append(crawled_dict)
                    return crawled_dict

                article_source_code = requests.get(item.url).text
                article = self.descriptor.parse_article(article_source_code)

                print(item.title)
                crawled_dict[item.url] = {
                    'title': item.title,
                    'pubdate': item.pubdate,
                    'body': article.body
                }


if __name__ == '__main__':
    def parse_date(date_str):
        pubdate = parse(date_str)
        if pubdate:
            return pubdate
        else:
            return argparse.ArgumentTypeError("couldn't parse following date: %s" % date_str)

    input_args =argparse.ArgumentParser()
    input_args.add_argument('-stop', help='datetime which stops crawling', type=parse_date, required=True)
    args = input_args.parse_args()

    stop_date = args.stop

    descriptor = MarimediaRuDescriptor()
    crawler = Crawler(descriptor)

    items = crawler.crawl(stop_date)