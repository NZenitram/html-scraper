import concurrent.futures
import requests
import time
import logging
import zlib
from bs4 import BeautifulSoup
from datetime import datetime
import sys

class Scraper():
    def __init__(self, providers):
        self.providers = providers
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def homepage(self, client):
        compressed_html = []

        response = [self.executor.submit(requests.get, prov[1]) for prov in self.providers]
        concurrent.futures.wait(response)

        [self.executor.submit(self.save_html_scraping(resp, client), resp) for resp in response]

    def save_html_scraping(self, data, client):
        print('Starting...   ' + str(time.strftime("%Y-%m-%d %H:%M:%S")))

        if not self.check_if_provider_and_page_record_exists(data.result().url, client):
            client.cur.execute("""INSERT INTO provider_page
                                  (provider_url, current_scrape, new_scrape, updated_at)
                                  VALUES (%s, %s, %s, %s)""", (data.result().url, data.result().text, None, datetime.now()))
            client.con.commit()
        else:
            client.cur.execute("""UPDATE provider_page 
                                  SET new_scrape=%s, updated_at=%s
                                  WHERE provider_url=%s""", (data.result().text, datetime.now(), data.result().url))
            client.con.commit()

    def check_if_provider_and_page_record_exists(self, url, client):
        check_provider = ('SELECT * FROM provider_page WHERE provider_url="{0}"'.format(url))

        client.cur.execute(check_provider)
        print("Current scrape exists for " + url + ", checking new scrape... ")
        return client.cur.fetchone()