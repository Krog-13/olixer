import sys

from bs4 import BeautifulSoup as BS
import requests
from config import SOURCE_URL
from typing import Dict
import logging, sys
from logging import StreamHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = StreamHandler(stream=sys.stdout)
logger.debug('start')


class Crawler:

    def __init__(self, param: Dict):
        self.source_url = SOURCE_URL
        self.param = param

    def source_page(self):
        try:
            source_page = requests.get(self.source_url + self.param.get('address'))
            print(source_page.status_code)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return BS(source_page.content, 'lxml')

    def get_posts(self):
        pass

class Olixer(Crawler):
    def __init__(self, param, user_id: int):
        super().__init__(param)
        self.user_id = user_id
        self.source_html = self.source_page()

    def last_post(self):
        # print(self.source_html)
        last_id = self.source_html.select('table#offers_table h3>a', limit=2, href=True)
        logger.debug(last_id, self.user_id)
        print(last_id[1]['href'])

    def get_text(self):
        pass
    def get_datetime(self):
        pass





if __name__ == '__main__':
    param = {'address':'/elektronika/astana/'}
    t1 = Olixer(param, 1)
    t1.last_post()
