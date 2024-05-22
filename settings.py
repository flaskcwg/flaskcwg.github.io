"""
This file contains important variables for site generation
"""

import json

OUTPUT_FOLDER = "docs/"
INFO = None

BLOG_CATEGORIES = ["main", "protocol"]

VOLUNTEERS_DESCS = {
    "event": "Events collaborator/programmer",
    "code": "Website/Projects maintainer",
    "education": "Tutorials/Posts Flask related",
}

with open("info.json", encoding="utf-8") as f:
    INFO = json.load(f)
