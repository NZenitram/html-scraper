from get_client import GetClient

class CompareScrapes(GetClient):
    def __init__(self):
        self.con = GetClient.con
        self.cur = GetClient.cur
