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
        driver.quit()

    def check_if_provider_and_page_record_exists(self, client):
        check_provider = ("SELECT * FROM provider_page WHERE provider_id=" + str(self.provider.id))

        client.cur.execute(check_provider)
        return client.cur.fetchone()


        return True
    def check_if_current_scrape_exists(self, client):
        check_record = ("SELECT current_scrape FROM provider_page WHERE provider_id=" + str(self.provider.id))

        client.cur.execute(check_record)
        return client.cur.fetchone()



    def save_html_scraping(self, data, client):
        add_record = ("INSERT INTO provider_page "
                      "(provider_id, current_scrape, new_scrape, updated_at) "
                      "VALUES (%s, %s, %s, %s)")

        update_record = ("UPDATE provider_page "
                         "(provider_id, current_scrape, new_scrape, updated_at) "
                         "VALUES (%s, %s, %s, %s)"
                         "WHERE provider_id=" + str(self.provider.id))

        current_scrape = (self.provider.id, data, None, datetime.now())
        new_scrape = (self.provider.id, None, data, datetime.now())


        if not self.check_if_provider_and_page_record_exists(client):
            client.cur.execute(add_record, current_scrape)
            client.con.commit()

        if self.check_if_current_scrape_exists(client):
            client.cur.execute(update_record, new_scrape)
            client.con.commit()

