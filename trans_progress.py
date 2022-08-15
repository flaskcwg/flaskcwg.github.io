"""
This script get translation progress data
from https://github.com/Jalkhov/docspro/tree/translation_data/data
"""

import ast
import json
import urllib.request

import requests

uri = "https://raw.githubusercontent.com/Jalkhov/docspro/translation_data/data/{lang}_data.json"


class TransProgress(object):
    def __init__(self, repos):
        super(TransProgress, self).__init__()
        self.repos = repos

    def get_data(self):
        data = {}
        for lang in self.repos:
            data[lang] = self.get_cov(lang)

        return data

    def get_cov(self, lang):
        response = requests.get(uri.format(lang=lang)).text
        percent = json.loads(response)["percent"]
        return percent


def main():
    mu = TransProgress(["es", "fr", "zh", "fa"])
    data = mu.get_data()
    print(data)


if __name__ == "__main__":
    main()
