import sys
from loguru import logger as LOGGER
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
        self.posts['id'] = None

    def new_posts(self, page):
        self.source_html = self.source_page(page['query_post'])
        urls = self.source_html.select('table#offers_table h3>a[href]', limit=10, href=True)
        # urls_top = self.source_html.select('table.offers--top h3>a', limit=8, href=True)
        for url in urls:
            if url['href'] == page['last_post']:
                break
            self.posts['urls'].append(url['href'])
        self.posts['id'] = page['user_id']
        return self.posts


    def get_posts(self, all_queries):
        for page in all_queries:
            posts = self.new_posts(page)
            yield posts




    def get_info_post(self, url):
        self.source_html = self.source_page(url)
        return self.source_html.select('h1[data-cy="ad_title"]')
    def get_datetime(self):
        pass





if __name__ == '__main__':
    param = {'address':'/elektronika/astana/'}
    t1 = Olixer(param, 1)
    t1.last_post()
