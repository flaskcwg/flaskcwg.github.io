"""
This script get translation progress data
from https://github.com/Jalkhov/docspro/tree/translation_data/data
"""

import json

import requests

url_direct_json = "https://raw.githubusercontent.com/Jalkhov/docspro/translation_data/data/{lang}_data.json"
url_translation_data = "https://api.github.com/repos/Jalkhov/docspro/git/trees/translation_data"
url_tree = "https://api.github.com/repos/Jalkhov/docspro/git/trees/{sha}"


class TransProgress(object):
    def __init__(self):
        super(TransProgress, self).__init__()

    def __get_code_langs(self):
        translation_data_request = requests.get(url_translation_data).json()

        # Get SHA from data/ folder
        data_dir_sha = translation_data_request['tree'][1]['sha']

        # Get Tree from data/ folder based in SHA
        data_tree_request = requests.get(url_tree.format(sha=data_dir_sha)).json()

        # Get tree from data/ folder
        data_files = data_tree_request['tree']

        # Get files with repo data from data/ tree
        jsons = [x['path'] for x in data_files if '_data' in x['path']]

        # Get just lang_codes from filenames
        lang_codes = [x.split('_')[0] for x in jsons]

        return lang_codes

    def __get_percent(self, lang):
        response = requests.get(url_direct_json.format(lang=lang)).json()
        percent = response["trans_percent"]
        return percent

    def get_data(self):
        lang_codes = self.__get_code_langs()
        data = {}
        for lang in lang_codes:
            data[lang] = self.__get_percent(lang)

        return data


def main():
    # mu = TransProgress()
    # data = mu.get_data()
    pass


if __name__ == "__main__":
    main()
