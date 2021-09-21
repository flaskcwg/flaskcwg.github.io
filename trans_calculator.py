# This script calculate translated percent from
# FLASKCWG repos

import json
import urllib.request

import polib
import requests


def get_raw_url(file_path, url):
    tmp_url = url.replace(
        'https://api.github.com/repos/',
        'https://raw.githubusercontent.com/')
    tmp_url = tmp_url.split('/git/blobs/')[0]
    tmp_url = tmp_url + '/main/' + file_path

    return tmp_url


uri = 'https://api.github.com/repos/flaskcwg/flask-docs-{}/git/trees/main?recursive=1'


class TranslatedProgress(object):
    """docstring for TranslatedProgress"""

    def __init__(self, repos):
        super(TranslatedProgress, self).__init__()
        self.repos = repos

    def IterateRepos(self):
        files = {}
        for repo in self.repos:
            print("Getting PO files from: {}".format(repo))
            files[repo] = self.GetPoFiles(repo)

        return files

    def GetPoFiles(self, repo):
        api = requests.get(uri.format(repo)).text
        files = json.loads(api)

        output = []
        location = dict()
        for (k, i) in enumerate(files['tree']):
            if 'LC_MESSAGES' in i['path']:
                if i['type'] == 'blob':
                    tmp = [i['path']]
                    tmp += [get_raw_url(tmp[0], i['url']), i['size']]
                    output.append(tmp)
        files = output

        return files

    def GetFileInfo(self):
        progress = {}
        files = self.IterateRepos()
        for repo in files:
            print("Walking files from: {}".format(repo))
            f = []
            for raws in files[repo]:
                print(
                    "    [{}] Getting translated progress from: {}".format(repo, raws[0]))
                raw_url = raws[1]
                po = polib.pofile(requests.get(raw_url).text)
                f.append([po.percent_translated(), raws[2]])
            progress[repo] = f

        return progress

    def TranslatedPercent(self):
        # Formula:
        # (file1_size * file1_progress + file2_size * file2_progress) / (file1_size+file2_size)
        data = self.GetFileInfo()
        out = {}
        for project in data:
            left = 0
            right = 0
            for x in data[project]:
                left += x[1] * x[0]
                right += x[1]
            out[project] = round(left / right)  # use the formula

        return out
