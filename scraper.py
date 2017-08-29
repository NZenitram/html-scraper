import concurrent.futures
import requests
import time
import logging
import db

from config import config
from get_client import GetClient
from datetime import datetime
from logging.config import dictConfig
from logging_config import log_config

dictConfig(log_config)

class Scraper(GetClient):
    def __init__(self):
        self.client = GetClient()
        self.logger = logging.getLogger('scraper')
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def scrape_page(self):
        providers = self.client.get_all_providers()
        response = [self.executor.submit(requests.get, prov[1]) for prov in providers]
        concurrent.futures.wait(response)

        [self.executor.submit(self.save_html_scraping(resp), resp) for resp in response]

    def save_html_scraping(self, data):
        self.logger.info('Running...   ' + str(time.strftime("%Y-%m-%d %H:%M:%S")) + ' ' + data.result().url )
        with db.connection(pool_name="mypool", pool_size=10, **config['config']['db']) as con:
            with db.cursor(con) as cursor:

                if not self.check_if_provider_and_page_record_exists(data.result().url, cursor):
                    cursor.execute("""INSERT INTO provider_page
                                          (provider_url, current_scrape, new_scrape, updated_at)
                                          VALUES (%s, %s, %s, %s)""", (data.result().url, data.result().text, None, datetime.now()))
                    con.commit()
                elif not self.check_if_new_scrape_exists(data.result().url, cursor):
                    cursor.execute("""UPDATE provider_page 
                                          SET new_scrape=%s, updated_at=%s
                                          WHERE provider_url=%s""", (data.result().text, datetime.now(), data.result().url))
                    con.commit()
                else:
                    return False

    def check_if_provider_and_page_record_exists(self, url, cursor):
        check_provider = ('SELECT * FROM provider_page WHERE provider_url="{0}"'.format(url))

        cursor.execute(check_provider)
        return cursor.fetchone()

    def check_if_new_scrape_exists(self, url, cursor):
        check_new_scrape = ('SELECT new_scrape FROM provider_page WHERE provider_url="{0}"'.format(url))

        cursor.execute(check_new_scrape)
        type = cursor.fetchone()
        if type['new_scrape'] is None:
            return False
        else:
            return True