import json

OUTPUT_FOLDER = 'docs/'
info = None

BLOG_CATEGORIES = [
    'main',
    'protocol'
]

with open('info.json', encoding='utf-8') as f:
    info = json.load(f)
