# -*- coding: utf-8 -*-

import pickle
from datetime import datetime


class FileClient(object):
    file_name = 'crawled_marimedia.pkl'

    def __init__(self):
        self.data_file = open(self.file_name, 'wb+')
        self.data_file.seek(0)
        content = self.data_file.read()

        print(content)

        if content:
            self.data = pickle.load(self.data_file)
            self.data_file.seek(0)
            print('init')
            print(self.data)
            print('init')
        else:
            self.data = {}

    def __enter__(self):
        return self

    def assert_item_format(self, item):
        assert 'title' in item
        assert 'pubdate' in item
        assert type(item['pubdate']) is datetime
        assert 'body' in item

    def read(self):
        return self.data

    def append(self, data):
        print(self.data)
        print(data)
        for url in data:
            self.data[url] = data[url]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.data_file.seek(0)
        pickle.dump(self.data, self.data_file)
        self.data_file.seek(0)
        self.data_file.close()