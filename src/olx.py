import sys

from bs4 import BeautifulSoup as BS
import requests
from config import SOURCE_URL
from typing import Dict, OrderedDict
import logging, sys
from logging import StreamHandler
import config


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = StreamHandler(stream=sys.stdout)
logger.debug('start')


class Crawler:

    def __init__(self):
        self.source_url = SOURCE_URL

    def source_page(self, page):
        try:
            source_page = requests.get(page)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return BS(source_page.content, 'lxml')



    def correct_address(self, address):
        return True

class Olixer(Crawler):
    def __init__(self, param=None):
        super().__init__()

        self.posts = {}
        self.initialization()

    def initialization(self):
        self.posts['urls'] = []
        self.posts['urls_top'] = []

    def new_posts(self, page):
        self.source_html = self.source_page(page)
        urls = self.source_html.select('table#offers_table h3>a', limit=10, href=True)
        urls_top = self.source_html.select('table.offers--top h3>a', limit=8, href=True)
        for url in urls:
            self.posts['urls'].append(url['href'])
        for url in urls_top:
            self.posts['urls_top'].append(url['href'])
        return self.posts


    def get_posts(self, all_queries):
        for page in all_queries:
            source = self.new_posts(page['query_post'])




    def get_text(self):
        pass
    def get_datetime(self):
        pass





if __name__ == '__main__':
    param = {'address':'/elektronika/astana/'}
    t1 = Olixer(param, 1)
    t1.last_post()
