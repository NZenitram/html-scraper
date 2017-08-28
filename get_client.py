import mysql.connector
from client import Client
from config import config
from scraper import Scraper


class GetClient:
    def __init__(self):
        self.con = mysql.connector.connect(pool_name="mypool", pool_size=10, **config['config']['db'])
        self.cur = self.con.cursor(dictionary=True, buffered=True)

    # def get_provider_information(self):
    #     prov_id = str(config['providers'][self.provider])
    #     self.cur.execute('SELECT * FROM provider WHERE id =' + prov_id)
    #
    #     client = [Client(**client) for client in self.cur.fetchall()][0]
    #
    #     Scraper(client).homepage(self)

    def get_all_providers(self):
        url_list = []
        self.cur.execute('SELECT url, id FROM provider')

        providers = [Client(**client) for client in self.cur.fetchall()]

        for provider in providers:
            url_list.append([provider.id, provider.url])

        Scraper(url_list).homepage(self)


if __name__ == '__main__':
    get_client = GetClient()
    get_client.get_all_providers()