import mysql.connector
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

class Scraper():
    def __init__(self, provider):
        self.provider = provider

    def homepage(self, client):
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        driver.get('http://www.google.com')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        self.save_html_scraping(soup.prettify(), client)

    def save_html_scraping(self, data, client):
        add_record = ("INSERT INTO provider_pages "
                      "(provider_id, current_scrape, new_scrape, updated_at) "
                      "VALUES (%s, %s, %s, %s)")

        new_scrape = (self.provider.id, None, data, datetime.now() )

        client.cur.execute(add_record, new_scrape)