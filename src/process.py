from time import sleep
from src.config import AppConfig


class CosmoCargoProcess:
    def __init__(self):
        pass

    def start(self):
        while True:
            self.if_end()
            self.do()
            sleep(AppConfig.FETCH_INTERVAL)

    def do(self):
        print("fetching")

    def if_end(self):
        print("check for ending")