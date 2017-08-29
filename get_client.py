from config import config
from client import Client
import db

class GetClient():
    # def __init__(self):
    #     self.con = db.connection(pool_name="mypool", pool_size=10, **config['config']['db'])
    #     self.cur = self.con.cursor(dictionary=True, buffered=True)

    # def get_provider_information(self, provider):
    #     prov_id = str(config['providers'][provider])
    #     self.cur.execute('SELECT * FROM provider WHERE id =' + prov_id)
    #
    #     client = [Client(**client) for client in self.cur.fetchall()][0]
    #
    #     # Scraper(client).homepage(self)

    def get_all_providers(self):
        with db.connection(pool_name="mypool", pool_size=10, **config['config']['db']) as con:
            with db.cursor(con, dictionary=True, buffered=True) as cursor:
                url_list = []

                cursor.execute('SELECT url, id FROM provider')

                providers = [Client(**client) for client in cursor.fetchall()]

                for provider in providers:
                    url_list.append([provider.id, provider.url])

                return url_list