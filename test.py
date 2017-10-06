from datetime import datetime
import pickle


data = {
    'http://example.com/asdf': {
        'title': 'News 1',
        'pubdate': datetime(year=2017, month=1, day=1),
        'body': 'News body 1'
    }
}

with open('crawled_marimedia.pkl', 'rb') as f:
    print(pickle.load(f))