title: How to synchronize translations
summary: Steps to update translations
authors: flpm
date: May 21, 2024
tags: translation
slug: how-sync-translations

title: How to synchronize translations
summary: Steps to update translations
authors: flpm
date: May 21, 2024
tags: translation
slug: how-sync-translations

One of the challenges of maintaining translations is keeping up with the changes to the original document as the project advances and new releases are made.

In the case of the Flask documentation, theres the additional challenge of working in separate repositories.

This post will document a simple process for contributors and maintainers of the different languages repositories to keep up to date with the latest version of the Flask English documentation.

## Set up your local environment

First, fork the language repository in the Flask CWG corresponding to the language you will be working on into your personal Github space. If you need, you can find more information it the GitHub documentation [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

Once the fork is created, clone the repository on your computer. Again, for more details on this step, consult the GitHub documentation [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

At this point you will have the latest version of the translation for the language you are working on.

## Add the main Flask repository as a new git remote

A quick note: the command examples you will see below, show the tags and commit hashes at the time this blog post was written. When you execute these commands, you will probably see different values.

To make sure you are up to date with the original English documentation, you will need to set a new git remote repository pointing to the main flask repository:

```shell
$ git remote add flask https://github.com/pallets/flask.git
```

And fetch the data from it.

```shell
$ git fetch flask
remote: Enumerating objects: 24785, done.
remote: Counting objects: 100% (249/249), done.
remote: Compressing objects: 100% (187/187), done.
remote: Total 24785 (delta 105), reused 166 (delta 53), pack-reused 24536
Receiving objects: 100% (24785/24785), 10.22 MiB | 16.41 MiB/s, done.
Resolving deltas: 100% (16592/16592), done.
From https://github.com/pallets/flask
 * [new branch]        0.12.x     -> flask/0.12.x
 * [new branch]        1.0.x      -> flask/1.0.x
 * [new branch]        1.1.x      -> flask/1.1.x
 * [new branch]        2.0.x      -> flask/2.0.x
 * [new branch]        2.1.x      -> flask/2.1.x
 * [new branch]        2.2.x      -> flask/2.2.x
 * [new branch]        2.3.x      -> flask/2.3.x
 * [new branch]        3.0.x      -> flask/3.0.x
 * [new branch]        main       -> flask/main
 * [new tag]           1.1.4      -> 1.1.4
(...)
 * [new tag]           2.3.3      -> 2.3.3
 * [new tag]           3.0.1      -> 3.0.1
 * [new tag]           3.0.2      -> 3.0.2
 * [new tag]           3.0.3      -> 3.0.3
```

## Update the English source of your translation

Start by creating a new branch:

```shell
$ git checkout -b update-docs main
Switched to a new branch 'update-docs'
```

And deleting the current `.rst` files (this step is necessary to ensure we don't keep old files that may have been renamed):

```shell
$ rm -r ./docs/*.rst
```

The Flask CWG in discussion with the Flask project maintainers have decided to keep the translations synchronized with the documentation of latest released version of Flask. To find the last version of the English documentation, locate the latest release tag:

```shell
$ git tag --sort=-taggerdate | head -n 1
3.0.3

```

Once you know the right tag, you can checkout the right version of the documentation folder into your new branch:

```shell
$ git checkout 3.0.3 ./docs/
Updated 14 paths from a7d387fa

$ git status
On branch update-docs
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   docs/api.rst
	modified:   docs/conf.py
	modified:   docs/config.rst
	modified:   docs/errorhandling.rst
	modified:   docs/index.rst
	modified:   docs/license.rst
	modified:   docs/logging.rst
	modified:   docs/patterns/appdispatch.rst
	modified:   docs/patterns/javascript.rst
	modified:   docs/patterns/packages.rst
	modified:   docs/patterns/sqlalchemy.rst
	modified:   docs/server.rst
	modified:   docs/testing.rst
	modified:   docs/tutorial/install.rst

```

Let's commit these changes to the branch:

```shell
git commit -m 'Updated the English documentation'
[update-docs 2993d997] Updated the English documentation
 14 files changed, 58 insertions(+), 89 deletions(-)

```

Next, let's make sure we have the right requirements to build this version of the documentation, in case something changed.

```shell
git checkout 3.0.3 ./requirements/
Updated 0 paths from a7d387fa

```

In this case no files where updated ("Updated 0 paths"), but if the requirements changed, we would have to commit the changes to this branch.

## Prepare a virtual environment to build the documentation

To make sure you can build the documentation, create a virtual environment and install the necessary requirements. Assuming you have virtualenv installed, run the following commands:

```shell
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r ./requirements/docs.txt
Collecting alabaster==0.7.16
  Using cached alabaster-0.7.16-py3-none-any.whl (13 kB)
Collecting babel==2.14.0
  Downloading Babel-2.14.0-py3-none-any.whl (11.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.0/11.0 MB 31.3 MB/s eta 0:00:00
Collecting certifi==2024.2.2
  Downloading certifi-2024.2.2-py3-none-any.whl (163 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 163.8/163.8 KB 12.0 MB/s eta 0:00:00
Collecting charset-normalizer==3.3.2
  Using cached charset_normalizer-3.3.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (142 kB)
(...)
```

Now, you are ready to update the translation files.

## Recreate the translation templates (`.pot` files)

Before we can update the translation files for the language you are working on, you need to recreate the translation template files with the latest version of the documentation you just copied.

```shell
$ cd ./docs
$ make gettext
Running Sphinx v7.2.6
making output directory... done
loading intersphinx inventory from https://docs.python.org/3/objects.inv...
loading intersphinx inventory from https://werkzeug.palletsprojects.com/objects.inv...
loading intersphinx inventory from https://click.palletsprojects.com/objects.inv...
loading intersphinx inventory from https://jinja.palletsprojects.com/objects.inv...
loading intersphinx inventory from https://itsdangerous.palletsprojects.com/objects.inv...
loading intersphinx inventory from https://docs.sqlalchemy.org/objects.inv...
(...)
```

## Update the translation files (`.po` files)

Before we can run the next step, we need to install `sphinx-intl` in the current virtual environment:

```shell
$ pip install sphinx-intl
Collecting sphinx-intl
  Downloading sphinx_intl-2.2.0-py3-none-any.whl (13 kB)
Requirement already satisfied: babel in /home/felipe/github/flaskcwg/flask-docs-es/venv/lib/python3.10/site-packages (from sphinx-intl) (2.14.0)
Requirement already satisfied: setuptools in /home/felipe/github/flaskcwg/flask-docs-es/venv/lib/python3.10/site-packages (from sphinx-intl) (59.6.0)
Requirement already satisfied: sphinx in /home/felipe/github/flaskcwg/flask-docs-es/venv/lib/python3.10/site-packages (from sphinx-intl) (7.2.6)
(...)
```

Once the templates are updated and sphinx-intl is install, you can update the translations files in the `./locales` folder.

In the example below, we are working with the Spanish translation (language code `es`), you will have to use the code for the language you are working on:

```shell
$ sphinx-intl update -p _build/gettext -l esUpdate: locales/es/LC_MESSAGES/api.po +19, -26
Not Changed: locales/es/LC_MESSAGES/config.po
Not Changed: locales/es/LC_MESSAGES/templating.po
Not Changed: locales/es/LC_MESSAGES/license.po
Not Changed: locales/es/LC_MESSAGES/blueprints.po
Update: locales/es/LC_MESSAGES/testing.po +1, -2
Not Changed: locales/es/LC_MESSAGES/views.po
(...)
```

At this point, the `.po` files in the `./locales` folder are up to date with the latest version of the English documentation. The update process will preserve the current translations and add new strings. If some of the translated strings have changed in the original source, the entries in the `.po` files will be marked with the tag "fuzzy", which a translator can remove after making the appropriate changes.

For more information about the PO format, including the fuzzy tag, consult the [gettext documentation](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html).

