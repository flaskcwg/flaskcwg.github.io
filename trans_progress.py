"""
This script get translation progress data
from https://github.com/Jalkhov/docspro/tree/translation_data/data
"""

import requests

URL_DIRECT_JSON = (
    "https://raw.githubusercontent.com/Jalkhov/docspro/"
    "translation_data/data/{lang}_data.json"
)

URL_TRANSLATION_DATA = (
    "https://api.github.com/repos/Jalkhov/docspro/"
    "git/trees/translation_data"
)

URL_TREE = "https://api.github.com/repos/Jalkhov/docspro/git/trees/{sha}"


def get_lang_codes():
    """
    Gets the available language codes given by Docspro
    """
    translation_data_request = requests.get(URL_TRANSLATION_DATA, timeout=10).json()

    # Get SHA from data/ folder
    data_dir_sha = translation_data_request['tree'][1]['sha']

    # Get Tree from data/ folder based in SHA
    data_tree_request = requests.get(URL_TREE.format(sha=data_dir_sha), timeout=10).json()

    # Get tree from data/ folder
    data_files = data_tree_request['tree']

    # Get files with repo data from data/ tree
    jsons = [x['path'] for x in data_files if '_data' in x['path']]

    # Get just lang_codes from filenames
    lang_codes = [x.split('_')[0] for x in jsons]

    return lang_codes

def get_percent(lang):
    """
    Gets the translation percentage of the given language
    """
    response = requests.get(URL_DIRECT_JSON.format(lang=lang), timeout=10).json()
    percent = response["trans_percent"]
    return percent

def get_data():
    """
    Return collected information
    """
    lang_codes = get_lang_codes()
    data = {}
    for lang in lang_codes:
        data[lang] = get_percent(lang)

    return data
