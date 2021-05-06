# Flask Community Workgroup

## How does the site gets built

Edit files in templates, generated files live in docs.

## What is the techstack behind?

**[jamstack](https://jamstack.org)**: Generate pages using Jinja templates.

**flask + livewatch**: If you want to auto regenerate files without executing `static.py`.

## How are the docs generated?

You need to have the **[jamstack library](https://pypi.org/project/jamstack/)** installed.

Run `static.py`.

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

See `index.html` in templates.