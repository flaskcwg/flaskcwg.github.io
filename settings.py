import json

OUTPUT_FOLDER = 'docs/'
info = None

BLOG_CATEGORIES = [
    'main',
    'protocol'
]

with open('info.json') as f:
    info = json.load(f)