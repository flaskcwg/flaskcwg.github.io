title: How to synchronize translations
summary: Steps to update translations
authors: flpm
date: May 21, 2024
tags: translation
slug: how-sync-translations

One of the challenges of maintaining different translations of documentation for an open source project is keeping up with the changes to the documentation in its original language as the project evolves and new releases are issued and updates are made.

As I learned during a recent open source sprint organized at PyCon US 2024, in the case of Flask’s documentation, there is an additional challenge of working in separate repositories for each language the documentation is translated into.

This post will document a simple process that the contributors and maintainers of the different language translations can use to keep their repositories up to date with the latest version of Flask’s documentation in English.

## Set up your local environment

First, fork the translation repository for the language you will be working on from the Flask CWG GitHub organization into your personal GitHub space. If you need, you can find more information about forking in the GitHub documentation [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

Once the forked repository has been created, clone it on your computer. If you are not familiar with this step, more details are available in the GitHub documentation [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

At this point, you will have the latest version of the translation for the language you are working on.

## Add the main Flask repository as a new git remote

_Quick note: The command outputs you will see below show details like tags and commit hashes from the time this post was written. When you execute them, you will probably see different values._

To access the original English documentation, you will need to set a new git remote repository that points to the main Flask repository:

```shell
$ git remote add flask https://github.com/pallets/flask.git
```

Then, fetch the data from it.

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

Then, delete the current English documentation .rst files in the translation repository (this step is necessary to ensure we don't keep old files that may have been removed in the English version):

```shell
$ rm -r ./docs/*.rst
```

In discussion with the Flask project maintainers, the Flask CWG has decided to keep the translations synchronized with the documentation of the latest released version of Flask. To find the most recent version of the English documentation, locate the latest release tag:

```shell
$ git tag --sort=-taggerdate | head -n 1
3.0.3

```

Once you have the right tag, you can checkout the right version of the documentation folder into your new branch:

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
(...)
```

Let's commit these changes to the branch:

```shell
git commit -m 'Updated the English documentation'
[update-docs 2993d997] Updated the English documentation
 14 files changed, 58 insertions(+), 89 deletions(-)

```

Next, to ensure you keep up with the documentation building requirements, update the requirements folder as well.

```shell
git checkout 3.0.3 ./requirements/
Updated 0 paths from a7d387fa

```

In this case, no files were updated ("Updated 0 paths"). But, if the requirements change, we will need those changes as well.

## Prepare a virtual environment to build the documentation

Prepare to build the documentation by creating a virtual environment and installing the necessary requirements. Assuming you have virtualenv installed, run the following commands:

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

## Recreate the translation templates (`.pot` files)

Before you can update the translation files for the language you are working on, you need to recreate the translation template files with the latest version of the documentation you just copied. This is an intermediate step as you will not be working on these files directly. They are stored in the `./_build/gettext` folder.

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

Before we can run the next step, you need to install sphinx-intl in your current virtual environment. Since this is a requirement for the translation work, it is not part of the original documentation requirements:

```shell
$ pip install sphinx-intl
Collecting sphinx-intl
  Downloading sphinx_intl-2.2.0-py3-none-any.whl (13 kB)
Requirement already satisfied: babel in /home/felipe/github/flaskcwg/flask-docs-es/venv/lib/python3.10/site-packages (from sphinx-intl) (2.14.0)
Requirement already satisfied: setuptools in /home/felipe/github/flaskcwg/flask-docs-es/venv/lib/python3.10/site-packages (from sphinx-intl) (59.6.0)
Requirement already satisfied: sphinx in /home/felipe/github/flaskcwg/flask-docs-es/venv/lib/python3.10/site-packages (from sphinx-intl) (7.2.6)
(...)
```

You are now ready to update the translation for the language you are working on. In the example below, we are working with the Spanish translation (language code `es`). Remember to replace the language code for the one for your language:

```shell
$ sphinx-intl update -p _build/gettext -l es
Update: locales/es/LC_MESSAGES/api.po +19, -26
Not Changed: locales/es/LC_MESSAGES/config.po
Not Changed: locales/es/LC_MESSAGES/templating.po
Not Changed: locales/es/LC_MESSAGES/license.po
Not Changed: locales/es/LC_MESSAGES/blueprints.po
Update: locales/es/LC_MESSAGES/testing.po +1, -2
Not Changed: locales/es/LC_MESSAGES/views.po
(...)
```

At this point, the `.po` files in the `./locales` folder have been updated with the latest version of the English documentation.

The update process will preserve the current translations and add new strings that might have been added to the English documentation.

If some of the already translated strings changed in the English documentation, the corresponding entries in the .po files will be marked with the tag "fuzzy", indicating they need to be checked for accuracy.

For more information about the PO format, including the fuzzy tag, consult the [gettext documentation](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html).

## Commit the translation files

Add the updated translation files to the branch. You do not need to worry about the .pot files, they don't need to be stored in the repository.

```shell
$ git add ./locales/

$ git status
On branch update-docs
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   locales/es/LC_MESSAGES/api.po
	new file:   locales/es/LC_MESSAGES/deploying.po
	modified:   locales/es/LC_MESSAGES/errorhandling.po
	new file:   locales/es/LC_MESSAGES/patterns.po
	modified:   locales/es/LC_MESSAGES/server.po
	modified:   locales/es/LC_MESSAGES/testing.po
	new file:   locales/es/LC_MESSAGES/tutorial.po

$ git commit -m 'Updated the translation files'
```

## Make a PR

At this point, you are ready to create a pull request to incorporate your changes into the Flask CWG language repository. You can find more information about creating a pull request in the  [GitHub documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
