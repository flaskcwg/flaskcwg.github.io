# Flask Community Workgroup

## How does the site gets built

**Note:** You need to have the **[jamstack library](https://pypi.org/project/jamstack/)** installed.

1. Edit files in the [**/templates**](/templates) folder
2. Run [**docs/serve.py**](docs/serve.py) in another terminal
3. Run [**static.py**](static.py) file then refresh the url of 2.
4. The final files are generated in the [**/docs**](/docs) folder.

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