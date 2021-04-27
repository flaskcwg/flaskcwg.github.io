import json

OUTPUT_FOLDER = 'docs/'
info = None

with open('info.json') as f:
    info = json.load(f)