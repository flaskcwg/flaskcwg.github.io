# Flask Community Workgroup

## How does the site gets built

**Note:** You need to have the **[jamstack library](https://pypi.org/project/jamstack/)** installed.

1. Run [**docs/serve.py**](docs/serve.py)
2. You will be provided with the **IP** and **PORT** to view the site
3. Edit files in the [**/templates**](/templates) folder
4. Run [**static.py**](static.py) file in another terminal
5. Refresh the url provided in step **2** to see the changes
6. The final files are generated in the [**/docs**](/docs) folder

Alternatively, you can also run `tox`.

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

