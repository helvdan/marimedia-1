from file_client import FileClient
import argparse


class Viewer(object):

    def __init__(self):
        file_client = FileClient()
        self.items = file_client.read()

    def show(self, pubdate_order='desc'):
        reverse = None
        if pubdate_order == 'desc':
            reverse = True
        elif pubdate_order == 'asc':
            reverse = False
        else:
            raise ValueError('unknown pubdate order %s' % pubdate_order)

        temp_list = []

        for url in self.items:
            item = self.items[url]
            item['url'] = url
            temp_list.append(item)

        temp_list.sort(key=lambda tmp_item: tmp_item['pubdate'], reverse=reverse)

        for tmp_item in temp_list:
            print('url: ' + tmp_item['url'])
            for tmp_item_key in tmp_item:
                print(tmp_item_key + ': ' + str(tmp_item[tmp_item_key]))


if __name__ == '__main__':

    input_args = argparse.ArgumentParser()
    input_args.add_argument('-view_order', help='view articles ordered by pubdate', choices=['asc', 'desc'])

    args = input_args.parse_args()

    viewer = Viewer()
    viewer.show(args.view_order)