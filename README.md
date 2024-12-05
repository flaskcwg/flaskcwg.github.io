
# Flask Community Workgroup

## Setup Instructions

### 1. **Fork the Repository**
- [Fork the repo](https://github.com/flaskcwg/flaskcwg.github.io/fork) to your GitHub account.

### 2. **Clone Your Fork**
- Clone your fork to your local machine:
    ```bash
    git clone https://github.com/{username}/flaskcwg.github.io.git
    cd flaskcwg.github.io
    ```

### 3. **Set Up Upstream Remote**
- Add the original repository as an upstream remote:
    ```bash
    git remote add upstream https://github.com/flaskcwg/flaskcwg.github.io.git
    ```

### 4. **Create and Activate a Virtual Environment**

- **Linux/Mac**:
    ```bash
    python -m venv env
    source env/bin/activate
    ```

- **Windows**:
    ```bash
    py -m venv env
    env\Scripts\activate.bat  # For Command Prompt
    # Or for Bash:
    source env/Scripts/activate
    ```

### 5. **Install Dependencies**
- Install the required dependencies:
    ```bash
    python -m pip install -r requirements.txt
    ```

### 6. **Build the HTML Content**
- Run the `static.py` script to generate the HTML content:
    ```bash
    python static.py
    ```

### 7. **Serve the Site**
- Serve the site locally:
    ```bash
    cd docs
    python serve.py
    ```
- Access the site at the IP address displayed in the terminal.

### 8. **View Template Changes**
- To apply changes made in the `/templates` directory:
    - Re-run `python static.py` in a separate terminal.
    - Refresh the browser to see the updates.

---

## Production Workflow

Pull requests are merged into the `source` branch, which is automatically deployed to the `gh-pages` branch.

---

## How to Add a New Page

In the `static.py` file, under the `generate` function, add another `generate` call, for example:

```python
def main(args):
    def gen():
        generate('index.html', join(settings.OUTPUT_FOLDER, 'index.html'), **context)
        generate('source_file.html', join(settings.OUTPUT_FOLDER, 'output_file.html'), **context)
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

**retired:** If someone is active or not.

Links are generated as links with text as the key and link as the value.

### Blog post

A blog post occurs in the format:

````markdown
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

All meta keys are mandatory but summary can be kept empty.

Inside of `data/blog` create a folder with the category you want. In `settings.py` add it:

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

The content should look like this:

````markdown
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

With this tool you can create, edit and delete blog/faq posts, just execute `python manage.py`.
