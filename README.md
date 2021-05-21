# Flask Community Workgroup

## Setup Instructions

* [Fork](https://github.com/flaskcwg/flaskcwg.github.io/fork) the repo
* Clone your forked repo

    ```bash
    git https://github.com/{username}/flaskcwg.github.io.git
    cd flaskcwg.github.io
    ```

* Setup the upstream to original repo

    ```bash
    git remote add upstream https://github.com/flaskcwg/flaskcwg.github.io.git
    ```

* Create a virtual env and activate it

    For Linux/Mac:

    ```bash
    python -m venv env
    source env/bin/activate
    ```

    For Windows:

    ```bash
    py -m venv env
    source env\Scripts\activate
    ```

* install dependencies

    ```bash
    pip install -r requirements.txt
    ```

* run `static.py`. This will build html content in `docs/`

    ```bash
    python static.py
    ```

* run `serve.py` as shown below. Go to the IP address shown in the printout to view the generated site. To see the changes made in [`/templates`](/templates) reflect on the generated site, run `python static.py` again (in separate terminal) and refresh the url.

    ```bash
    cd docs
    python serve.py
    ```

## How does the site runs in production?

PRs are made to source branch. The source branch is automatically extrapolated to the main branch where gh-pages is deployed

## How to add a new page?

In `static.py`, under generate, add another generate function:

```python
def main(args):
    def gen():
        generate('index.html', join(settings.OUTPUT_FOLDER, 'index.html'), **context)
```

Like this:

```python
def main(args):
    def gen():
        generate('index.html', join(settings.OUTPUT_FOLDER, 'index.html'), **context)
        generate('source_file.html', join(settings.OUTPUT_FOLDER, 'output_file.html'), **context)
```

Where `source_file.html` is the name of the file located in `templates/` and `output_file.html` is the output file which will be located in `docs/`.

## What is the techstack behind?

**[jamstack](https://jamstack.org)**: Generate pages using Jinja templates.

**flask + livewatch**: If you want to auto regenerate files without executing `static.py`.


## Data Formats


### Profile

In info.json, a profile looks like this

```json
        "greyli":{
            "name": "Grey Li",
            "bio": [],
            "volunteer": {
                "translation":{
                    "lang": "chinese",
                    "coordinator": "y"
                },
                "event": {},
                "code": {},
                "education": {}
            },
            "links":{
                "twitter": ""
            },
            "retired": "n"
        },
```


- name
- volunteer

Looks for four optional keys: translation, event, code, education.
For translation, you have lang and coordinator, the latter being optional

- bio

The bio is generated such that `''` are converted into `<br\>`. a bio would look like this:


```json
"bio": [
    "Line iwue hfowherf  oewrhfje.", 
    "woihfjerewoi tgfreh  eroh gfrehre greh g.", 
    "", "",
    "Some more lines"],
```

- links are generated as links with text as the key and link as the value

- retired

if someomne is active or not

### Blog post

A blog post occurs in the format:

`````md
title:   Demo blog post
summary: A demo post
authors: jugmac00
         Abdur-RahmaanJ
date:    May 19, 2021
slug: demo-blog-post

This is the first paragraph of the document.


```python
def x():
    pass
```


And hence [link demo](https://flaskcwg.github.io)
``````

All meta keys are mandatory but summary can be kept empty

Inside of data/blog create a folder with the category you want. In settings.py add it

```python
BLOG_CATEGORIES = [
    'main'
]
```

For authors, the author must occur in profiles.

