# -*- coding: utf-8 -*-

from lazy_property import LazyProperty
from dateparser import parse
from lxml.html import etree


class Article(object):

    def __init__(self, source_code):
        self.page = etree.HTML(source_code)

    @LazyProperty
    def body(self):
        return '\n'.join([
            ''.join(p.xpath('.//text()'))
            for p in self.page.cssselect('.news-text > p')
        ])


class MarimediaRuDescriptor(object):
    url = 'http://www.marimedia.ru'

    @classmethod
    def parse_article(cls, source_code):
        return Article(source_code)

    @LazyProperty
    def newsline(self):
        return Newsline()


class Newsline(object):
    url = 'http://www.marimedia.ru/news/'
    template = '?p={self.page}'

    def __init__(self, start=1, step=1, stop=1):
        self.page = start
        self.step = step
        self.stop = stop
        self._assert_page()

    def __iter__(self):
        return self

    def next(self):
        if self.page > self.stop:
            return StopIteration

        url = self.url if self.page == 1 else self.template.format(**locals())

        self.page += self.step
        return url

    def _assert_page(self):
        assert type(self.page) is int, 'start page should be integer'
        assert self.page > 0, 'start page should be greater than 0'

    @staticmethod
    def parse(source_code):
        page = etree.HTML(source_code)

        items = page.cssselect('.news-list > article')
        print 'there are %s items in newsline' % len(items)

        for item in items:
            item_classes = item.xpath('./@class')[0].split()
            if 'top-news' in item_classes:
                yield TopNewsItem(item)
            else:
                yield NewsItem(item)


class Item(object):

    def __init__(self, item):
        self._item = item

    @property
    def title_selector(self):
        raise NotImplementedError('property title_selector is not implemented in class %s' % self.__class__.__name__)

    @property
    def _title(self):
        return self._item.cssselect(self.title_selector)[0]

    @property
    def title(self):
        return self._title.text

    @property
    def url(self):
        return self._title.get('href')

    @property
    def pubdate(self):
        return parse(self._item.cssselect('.date')[0].text)

    @property
    def description(self):
        return None


class NewsItem(Item):
    title_selector = '.news_title'

    @property
    def description(self):
        return self._item.cssselect('.small-desc')[0].text


class TopNewsItem(Item):
    title_selector = '.news-title'

