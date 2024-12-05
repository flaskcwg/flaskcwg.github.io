"""
Configuration variables for site generation.

This script defines constants and settings used during the generation
of the website, such as folder paths, blog categories, volunteer
descriptions, and metadata loaded from an external JSON file.
"""

import json
import os

# Constants
OUTPUT_FOLDER = "docs/"
BLOG_CATEGORIES = ["main", "protocol"]
VOLUNTEERS_DESCS = {
    "event": "Events collaborator/programmer",
    "code": "Website/Projects maintainer",
    "education": "Tutorials/Posts Flask related",
}


# Load metadata from info.json
def load_info(file_path="info.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


try:
    INFO = load_info()
except (FileNotFoundError, json.JSONDecodeError) as e:
    INFO = {}
    print(f"Error loading info.json: {e}")
