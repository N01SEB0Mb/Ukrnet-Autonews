# created by noisebomb

# coding=utf-8

import parser
import requests
from lxml import html


class New(dict):
    def __init__(self, info):
        super().__init__(info)

    def __hash__(self):
        return self["Id"]

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class Parser:
    def __init__(self, config):
        self.last = config["last"]
        self.link = config["main_link"]
        self.max_len = config["max len"]
        self.session = requests.session()
        self.session.headers.update(config["headers"])

    def get_last(self):
        news_request = self.session.get(self.link)
        if news_request.status_code == 200:
            return {New(new) for new in news_request.json()["tops"][:self.last]}
        else:
            return set()

    def get_info(self, new):
        try:
            info_request = self.session.get(new["Url"])
            assert info_request.status_code == 200 and "utf-8" in info_request.headers["content-type"].lower()
        except (AssertionError, BaseException):
            return None

        return parser.parse(info_request.text, new["PartnerTitle"], max_len=self.max_len)
