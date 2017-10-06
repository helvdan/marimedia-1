# -*- coding: utf-8 -*-

import cPickle
from datetime import datetime
from pathlib import Path


class FileClient(object):
    file_name = 'crawled_marimedia.pkl'

    def __init__(self):
        self._data = {}

        data_file = Path(self.file_name)
        if data_file.exists():
            with open(self.file_name, 'r') as data_file:
                self._data = cPickle.load(data_file)
        else:
            with open(self.file_name, 'w+') as data_file:
                cPickle.dump(self._data, data_file)

    def __enter__(self):
        return self

    def assert_item_format(self, item):
        assert 'title' in item
        assert 'pubdate' in item
        assert type(item['pubdate']) is datetime
        assert 'body' in item

    def read(self):
        return self._data

    def append(self, data):
        for url in data:
            self._data[url] = data[url]

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.file_name, 'w') as data_file:
            cPickle.dump(self._data, data_file)
