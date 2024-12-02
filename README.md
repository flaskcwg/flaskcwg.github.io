# Flask Community Workgroup

## Setup Instructions

* [Fork](https://github.com/flaskcwg/flaskcwg.github.io/fork) the repo

* Clone your forked repo

    ```bash
    git clone https://github.com/{username}/flaskcwg.github.io.git
    cd flaskcwg.github.io
    ```

* Setup the upstream to original repo

    ```bash
    git remote add upstream https://github.com/flaskcwg/flaskcwg.github.io.git
    ```

* Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and activate it

    For Linux/Mac:

    ```bash
    python -m venv env
    source env/bin/activate
    # The following also works: `. env/bin/activate`
    ```

    For Windows:

    ```bash
    py -m venv env
    env\Scripts\activate.bat # if using command prompt
    # if using bash in windows, you can also do `source env/Scripts/activate`
    ```

* Install dependencies

    ```bash
    python -m pip install -r requirements.txt
    ```

* Run `static.py`. This will build html content in `docs/`.

    ```bash
    python static.py
    ```

* Run `serve.py` as shown below. Go to the IP address shown in the printout to view the generated site.

    ```bash
    cd docs
    python serve.py
    ```

* To see changes made in [`/templates`](/templates) reflect on the generated site, run `python static.py` again in separate terminal (not needed if you ran `python static.py --server` ) and refresh the url.

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

**[jamstack](https://pypi.org/project/jamstack)**: Generate pages using Jinja templates.

**flask + [livereload](https://pypi.org/project/livereload/)**: If you want to auto regenerate files without executing `static.py`.


## Data Formats


### Profile

In `info.json`, a profile looks like this

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

**name:** Member full name.

**volunteer:** Looks for four optional keys: translation, event, code, education.
For translation, you have lang and coordinator, the latter being optional.

**bio:** The bio is generated such that `''` are converted into `<br\>`. a bio would look like this:


```json
"bio": [
    "Line iwue hfowherf  oewrhfje.",
    "woihfjerewoi tgfreh  eroh gfrehre greh g.",
    "", "",
    "Some more lines"],
```

**retired:** If someomne is active or not.

Links are generated as links with text as the key and link as the value.

### Blog post

A blog post occurs in the format:

````md
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
````

All meta keys are mandatory but summary can be kept empty

Inside of `data/blog` create a folder with the category you want. In `settings.py` add it

```python
BLOG_CATEGORIES = [
    'main'
]
```

For authors, the author must occur in profiles.

### Projects

```json
{
    "name": "Flask-Dance",
    "link": "https://github.com/singingwolfboy/flask-dance",
    "info": ["Doing the OAuth dance with style using Flask, requests, and oauthlib."],
    "tags": ["auth", "oauth"]
}
```

### FaQ

In `data/faq`, create a `.md` file with whatever name you want `.md`

The content should look like this


````md
title:   Demo faq question
tags: demo
      flask
      lol
slug: demo-faq-question


This is the first paragraph of the document.

```python
def x():
    pass
```

And hence [link demo](https://flaskcwg.github.io)
````

### FlaskCWG Manager

With this tool you can create, edit and delete blog/faq posts, only pass `--manage` option to `static.py` and go to the given url.

### Percentage of translation of flask documentation

By default, when running `python static.py`, the translation percentage of the translation repositories is not updated, this is to avoid that every time you deploy locally the calculation process is not performed, to run this calculation just pass the `--with-trans-calc` parameter, i.e. `python static.py --with-trans-calc`.
