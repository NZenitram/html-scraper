import mysql.connector
from client import Client
from config import config
from scraper import Scraper


class GetClient:
    def __init__(self, provider):
        self.provider = provider
        self.con = mysql.connector.connect(**config['config']['db'])
        self.cur = self.con.cursor(dictionary=True, buffered=True)

    def get_provider_information(self):
        prov_id = str(config['providers'][self.provider])
        self.cur.execute('SELECT * FROM provider WHERE id =' + prov_id)

        client = [Client(**client) for client in self.cur.fetchall()][0]

        Scraper(client).homepage(self)




