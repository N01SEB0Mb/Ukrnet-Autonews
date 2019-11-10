# created by noisebomb

# coding=utf-8

import json
import requests
from requests.exceptions import BaseHTTPError
from lxml import html
import gzip


class New:
    def __init__(self, info):
        self.__dict__ = info

    def __hash__(self):
        return self.__dict__["Id"]

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __getitem__(self, item):
        return self.__dict__[item]


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
        except BaseException:
            return None

        if info_request.status_code == 200 and "utf-8" in info_request.headers["content-type"].lower():
            info_tree = html.fromstring(info_request.text)

            # title

            og_title = info_tree.xpath('//meta[@property="og:title" or @name="og:title"]/@content')
            _title = info_tree.xpath('//title/text()')
            twitter_title = info_tree.xpath('//meta[@property="twitter:title" or @name="twitter:title"]/@content')

            title = self.clear(max(og_title + twitter_title + [""], key=len))

            if not title:
                try:
                    title = self.clear(_title[0])
                except IndexError:
                    return None

            # description

            og_description = info_tree.xpath('//meta[@property="og:description" or @name="og:description"]/@content')
            _description = info_tree.xpath('//meta[@property="description" or @name="description"]/@content')
            twitter_description = info_tree.xpath('//meta[@name="twitter:description" or'
                                                  '@property="twitter:description"]/@content')

            description = self.clear(max(og_description + _description + twitter_description + [""], key=len))

            if description:
                while len(title) + len(description) + 16 > self.max_len:
                    description = description[:-1]
                while description[-1] == " ":
                    description = description[:-1]
                description += "...\n\n"

            # image

            og_image = info_tree.xpath('//meta[@property="og:image" or @name="og:image"]/@content')
            twitter_image = info_tree.xpath('//meta[@name="twitter:image" or @property="twitter:image"]/@content')

            image_url = og_image[0] if og_image else twitter_image[0] if twitter_image else None

            if not description and image_url is None:
                return None

            return title, description, image_url

    @staticmethod
    def clear(string):
        try:
            while string[0] in ("\n", " "):
                string = string[1:]
        except IndexError:
            pass
        else:
            try:
                while string[-1] in ("\n", " "):
                    string = string[:-1]
            except IndexError:
                pass
        return string
