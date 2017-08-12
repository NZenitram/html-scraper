from get_client import GetClient
from scraper import Scraper

if __name__ == '__main__':
    get_client = GetClient('gmail')
    get_client.get_provider_information()
