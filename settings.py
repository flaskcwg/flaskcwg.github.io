import json

OUTPUT_FOLDER = 'docs/'
info = None

BLOG_CATEGORIES = [
    'main',
    'protocol'
]

VOLUNTEERS_DESCS = {
    'event' : 'Events collaborator/programmer',
    'code': 'Website/Projects maintainer',
    'education': 'Tutorials/Posts Flask related'
}

with open('info.json', encoding='utf-8') as f:
    info = json.load(f)
