import json
import time
import pandas as pd

from collections import OrderedDict
from matplotlib import pyplot as plt
from matplotlib import animation
from requests import get
from datetime import date, datetime


BOOK_URI = r'https://api.gemini.com/v1/book/ethusd?'
API_KEY = r'1234'

# Gemini public API entry points: requests limited to 120 requests per minute
# Recommend not to exceed 1 request per second
#
# Gemini private API entry points: requests limited to 600 requests per minute
# Recommend not to exceed 5 requests per second

def get_book(asks, bids, **kwargs):
    kwargs.update({'limit_asks': asks,
                   'limit_bids': bids
                  })
    response = get(BOOK_URI, kwargs).json()
    
    return response

def create_book_df():
    response = get_book(50, 50)
    bid_price, bid_amount = [], []
    for i in response['bids']:
        bid_price.append(i['price'])
        bid_amount.append(i['amount'])
    
    book_df = pd.DataFrame(response['asks']).sort_values(by = 'timestamp', ascending = True)
    book_df['timestamp'] = pd.to_datetime(book_df['timestamp'], unit = 's')
    book_df['bid_price'], book_df['bid_amount'] = bid_price, bid_amount

    for row in book_df:
            book_df['price'] = book_df['price'].astype(float)
            book_df['bid_price'] = book_df['bid_price'].astype(float)
            book_df['spread'] = (book_df['price'] - book_df['bid_price']).astype(float)

    return book_df