import concurrent.futures
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import sys

class Scraper():
    def __init__(self, providers):
        self.providers = providers
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def homepage(self, client):

        response = [self.executor.submit(requests.get, prov[1]) for prov in self.providers]
        concurrent.futures.wait(response)

        [self.executor.submit(self.save_html_scraping(resp, client), resp) for resp in response]

    def save_html_scraping(self, data, client):
        add_record = ("INSERT INTO provider_page "
                      "(provider_url, current_scrape, new_scrape, updated_at) "
                      "VALUES (%s, %s, %s, %s)")

        update_record = ("UPDATE provider_page "
                         "(provider_url, current_scrape, new_scrape, updated_at) "
                         "VALUES (%s, %s, %s, %s)"
                         "WHERE provider_url=" + data.result().url)

        current_scrape = (data.result().url, data.result().text, None, datetime.now())
        new_scrape = (data.result().url, None, data.result().text, datetime.now())

        print('Starting...   ' + str(time.strftime("%Y-%m-%d %H:%M:%S")))

        if not self.check_if_provider_and_page_record_exists(data.result().url, client):
            client.cur.execute(add_record, current_scrape)
            client.con.commit()

        if self.check_if_current_scrape_exists(client):
            client.cur.execute(update_record, new_scrape)
            client.con.commit()

    def check_if_provider_and_page_record_exists(self, url, client):
        check_provider = ('SELECT * FROM provider_page WHERE provider_url="{0}"'.format(url))

        client.cur.execute(check_provider)
        print("Current scrape exists for " + url + ", checking new scrape... ")
        return client.cur.fetchone()

    def check_if_current_scrape_exists(self, url, client):
        check_record = ('SELECT * FROM provider_page WHERE provider_url="{0}"'.format(url))

        client.cur.execute(check_record)
        return client.cur.fetchone()