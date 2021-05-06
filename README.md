# flaskcwg.github.io

# How does the site gets built

Edit files in templates, generated files live in docs

# What is the techstack behind?

jamstack: generate pages using Jinja templates

flask + livewatch: if you want to auto regenerate files without executing static.py

# How are the docs generated?

Run static.py

# How to add a new page?

In static.py, under generate, add another generate function

```
def main(args):
    def gen():
        generate('index.html', join(settings.OUTPUT_FOLDER, 'index.html'), **context)
```

See index.html in templates
