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

_news_page_map = {
    'title': '_extract_string',
    'text': '_extract_text',
    'price': '_extract_price',
    # 'author': '_extract_string',
    'datetime': '_extract_datetime',
    # 'photo': '_extract_photo'
}

class Crawler:

    def __init__(self):
        self.source_url = SOURCE_URL

    def source_page(self, page):
        try:
            if page.startswith("http"):
                source_page = requests.get(page)
            else:
                source_page = requests.get(SOURCE_URL+page)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return BS(source_page.content, 'lxml')

    def correct_address(self, address):
        return True


class Olixer(Crawler):
    def __init__(self):
        super().__init__()
        self.posts = {}
        self.initialization()
        self.data = {}

    def initialization(self):
        self.posts['urls'] = []
        self.posts['id'] = None
        self.data = {}

    def new_posts(self, page):
        self.initialization()
        self.source_html = self.source_page(page['query_post'])
        # urls = self.source_html.select('table#offers_table h3>a[href]', limit=10, href=True)
        urls = self.source_html.select('div[data-testid=listing-grid] a[href]', limit=10, href=True)
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

    def extract_data(self, url):
        data = {}
        self.source_html = self.source_page(url)
        for name, selector in config.selector.items():
            extractor = getattr(self, '_extract_all')
            try:
                value = extractor(selector, name)
            except:
                continue
            data[name] = value
        return data

    def _extract_string(self, selector):
        item = self.source_html.select(selector)
        if not item:
            LOGGER.info('Not title')
            return ''
        return item[0].text
    # def _extract_text(self, selector):
    #     item = self.source_html.select(selector)[0].text
    #     return item
    # def _extract_datetime(self, selector):
    #     item = self.source_html.select(selector)[0].text
    #     return item
    # def _extract_price(self, selector):
    #     item = self.source_html.select(selector)[0].text
    #     return item
    # def _extract_author(self, selector):
    #     item = self.source_html.select(selector)[0].text
    #     return item

    def _extract_all(self, selector, name):
        item = self.source_html.select(selector)
        if not item:
            LOGGER.debug(f'not found {name}')
            return '*-*'
        return item[0].text

    def get_info_post(self, url):
        data = self.extract_data(url)
        return data




