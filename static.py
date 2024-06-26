"""
This file is responsible for building the site
"""

import datetime
import logging
import os
import re
import sys
from functools import wraps
from os.path import join
import markdown
import validators
from flask import Flask
from jamstack.api.template import base_context
from jamstack.api.template import generate as generate_
from livereload import Server
import settings
from trans_progress import get_data as get_translation_data

FOLDER_COUNT = 0
FILE_COUNT = 0

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def count_folders(function):
    """Returns number of times any function with this decorator is called"""

    @wraps(function)
    def increase_count(*args, **kwargs):
        global FOLDER_COUNT
        FOLDER_COUNT += 1
        return function(*args, **kwargs)

    return increase_count


def count_files(function):
    """Returns number of times any function with this decorator is called"""

    @wraps(function)
    def increase_count(*args, **kwargs):
        global FILE_COUNT
        FILE_COUNT += 1
        return function(*args, **kwargs)

    return increase_count


# path is the path to main page and is required on every page


@count_files
def generate(*args, **kwargs):
    """
    Wraps generate_ function
    """
    generate_(*args, **kwargs)


def profile_url(path, github_username):
    """
    Return site profile url
    """
    return f"{path}u/{github_username}"


def info_to_html(biolist):
    """
    expects a list in the format
    [
    'fretfreg', 'r34rt34tr', '', '',
    'wert3t35'
    ]
    """
    final_list = []
    for l in biolist:
        if l.strip() == "":
            final_list.append("<br/>")
        else:
            final_list.append(l)
    return " ".join(final_list)


def valid_date_str(datestr):
    """Check the correctness of the date written in .md files with regex"""
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    if not re.fullmatch(r"^[a-zA-Z]+ (\d){1,2}, (\d){4}$", datestr):
        return False
    month = "".join(re.findall(r"[a-zA-Z]", datestr))
    if not month.casefold() in months:
        return False
    day = re.findall(r"\d{1,2}", datestr)[0]
    if not 1 <= int(day) <= 31:
        return False
    return True


context = base_context()
context.update(
    {
        "info": settings.INFO,
        "path": "/",
        "profile_url": profile_url,
        "info_to_html": info_to_html,
    }
)


class InvalidSlug(Exception):
    """
    Check if exist invalid slug
    """
    def __init__(self, slug, filepath, message="Invalid slug"):
        self.slug = slug
        self.filepath = filepath
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.filepath}: {self.message}: {self.slug}"


class AuthorNotFound(Exception):
    """
    Checks if an author was not found
    """
    def __init__(
        self, author, filepath, message="Author's github handle not found in profiles"
    ):
        self.filepath = filepath
        self.author = author
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.filepath}: {self.message}: {self.author}"


@count_folders
def ensure_output_folder(path):
    """
    Ensures the existence of the given path in the output directory
    """
    if not os.path.exists(join(settings.OUTPUT_FOLDER, path)):
        os.mkdir(join(settings.OUTPUT_FOLDER, path))


def ensure_exist():
    """
    Ensures the existence of the output directory
    """
    if not os.path.exists(settings.OUTPUT_FOLDER):
        os.mkdir(settings.OUTPUT_FOLDER)
        logging.info("%s created", settings.OUTPUT_FOLDER)


def ensure_meta(taglist, metadata, document_path):
    """
    Ensures metadata exists
    """
    to_ensure = taglist
    for meta in to_ensure:
        if meta not in metadata:
            # logging.error("Missing meta attribute:", f"'{meta}'", "in path:",document_path)
            logging.error("Missing meta attribute: %s in path %s", meta, document_path)
            sys.exit()


def ensure_authors(authors, filepath):
    """
    Ensures that the authors exist
    """
    for author in authors:
        if author not in context["info"]["profiles"]:
            raise AuthorNotFound(author, filepath)


def is_valid_slug(slugstr):
    """
    Checks if the received slug is valid
    """
    if not validators.slug(slugstr):
        return False
    return True


def validate_slug(slug, filepath):
    """
    Validates the given slug
    """
    if not is_valid_slug(slug):
        raise InvalidSlug(slug, filepath)


def generate_profiles():
    """
    Function to generate profile files
    """
    logging.info("Start Generating profiles...")

    profiles = settings.INFO["profiles"]
    ensure_output_folder("u")
    for github_username in profiles:
        context.update(
            {
                "github_username": github_username,
                "data": profiles[github_username],
                "path": "../" * 2,
                "volunteers": settings.VOLUNTEERS_DESCS,
            }
        )
        ensure_output_folder(f"u/{github_username}")

        generate(
            "profile.html",
            join(settings.OUTPUT_FOLDER, "u", f"{github_username}", "index.html"),
            **context,
        )
        logging.info("Generating profile %s...", github_username)
    logging.info("Generating profiles is done")


def add_to_registry(tag, tags_registry, dict_object):
    """
    Add tags to registry
    """
    if tag not in tags_registry:
        tags_registry[tag] = []
        tags_registry[tag].append(dict_object)
    else:
        tags_registry[tag].append(dict_object)


def classify_by_tag(tags, tags_registry, dict_object):
    """
    dict_object -> python works by reference, modifying passed object
    """
    for tag in tags:
        add_to_registry(tag, tags_registry, dict_object)


def generate_blog_posts():
    """
    Function to generate blog archives
    """
    posts = []
    blog_data = "data/blog"

    logging.info("Start Generating blog posts ...")

    # n**2 solution
    for category in settings.BLOG_CATEGORIES:
        category_path = join(blog_data, category)
        # html = markdown.markdown(md, extensions=extensions, output_format='html5')
        for mdfile in os.listdir(category_path):
            blog_post_path = join(category_path, mdfile)
            with open(blog_post_path, encoding="utf-8") as f:
                text = f.read()
            md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
            html = md.convert(text)
            metadata = md.Meta
            slug = metadata["slug"][0]
            authors = metadata["authors"]
            title = metadata["title"][0]
            summary = metadata["summary"][0]
            tags = metadata["tags"]

            ensure_meta(
                ["slug", "authors", "date", "title", "summary", "tags"],
                metadata,
                blog_post_path,
            )
            ensure_output_folder("b")
            validate_slug(slug, blog_post_path)
            ensure_output_folder(f"b/{slug}")

            ensure_authors(authors, blog_post_path)

            raw_date = metadata["date"][0]
            if valid_date_str(raw_date):
                date = raw_date
            else:
                logging.error(
                    "The date '%s' must be in the format 'May 19, 2021'"
                    "in the file '%s'.", raw_date, mdfile
                )
                sys.exit()

            post = {
                "slug": slug,
                "content": html,
                "authors": authors,
                "date": date,
                "title": title,
                "summary": summary,
                "category": category,
                "tags": tags,
            }
            posts.append(post)
            context.update({"post": post, "path": "../" * 2})
            generate(
                "blog/post.html",
                join(settings.OUTPUT_FOLDER, "b", slug, "index.html"),
                **context,
            )
            logging.info("Generating blog post %s...", slug)
    # Blog post main page
    ensure_output_folder("blog")
    posts.sort(
        key=lambda x: datetime.datetime.strptime(x["date"], "%B %d, %Y")
    )  # May 19, 2021
    context.update({"posts": posts})
    generate(
        "blog/index.html", join(settings.OUTPUT_FOLDER, "blog", "index.html"), **context
    )
    logging.info("Generating blog/index.html...")

    # Category & tags scouting
    # Could also be done above but cleaner code here
    ensure_output_folder("category")
    ensure_output_folder("tag")
    categories_registry = {}
    tags_registry = {}

    for post in posts:
        tags = post["tags"]
        for tag in tags:
            ensure_output_folder(join("tag", tag))
        classify_by_tag(tags, tags_registry, post)

    for post in posts:
        category = post["category"]
        if category not in categories_registry:
            ensure_output_folder(join("category", category))
            categories_registry[category] = []
            categories_registry[category].append(post)
        else:
            categories_registry[category].append(post)

    # Generating category pages
    for category, posts in categories_registry.items():
        context.update(
            {
                "category": category,
                "posts": posts,
                "path": "../" * 2,
            }
        )
        generate(
            "category.html",
            join(settings.OUTPUT_FOLDER, "category", category, "index.html"),
            **context,
        )
        logging.info("Generating category %s...", category)

    for tag, posts in tags_registry.items():
        context.update({"tag": tag, "posts": posts, "path": "../" * 2})
        generate(
            "blog/tag.html",
            join(settings.OUTPUT_FOLDER, "tag", tag, "index.html"),
            **context,
        )
        logging.info("Generating tag %s...", tag)

    logging.info("Generating blog posts is done")



def generate_resources():
    """
    Generate resources page
    """
    resources = settings.INFO["resources"]
    logging.info("Start Generating resources ...")
    # /resources
    ensure_output_folder("resources")
    ensure_output_folder("resources/c")
    generate(
        "resources/index.html",
        join(settings.OUTPUT_FOLDER, "resources", "index.html"),
        **context,
    )
    logging.info("Generating resources/index.html...")
    tags_registry = {}
    # /resources/c/api/ # for category. category name cannot be tag

    for resource in resources:
        current_resource = resources[resource]["posts"]
        ensure_output_folder(join("resources", "c", resource))
        context.update(
            {
                "resource_name": resource,
                "current_resource": current_resource,
                "path": "../" * 3,
            }
        )
        generate(
            "resources/category.html",
            join(settings.OUTPUT_FOLDER, "resources", "c", resource, "index.html"),
            **context,
        )
        logging.info("Generating resources/c/%s/index.html...", resource)

        for project in current_resource:
            # print(project)
            tags = project["tags"]
            classify_by_tag(tags, tags_registry, project)

    # /resources/tag/asgi
    ensure_output_folder(join("resources", "tag"))
    for tag, projects in tags_registry.items():
        ensure_output_folder(join("resources", "tag", tag))
        context.update({"tag": tag, "projects": projects, "path": "../" * 3})
        generate(
            "resources/tag.html",
            join(settings.OUTPUT_FOLDER, "resources", "tag", tag, "index.html"),
            **context,
        )
        logging.info("Generating resources/tag/%s/index.html...", tag)
    logging.info("Generating resources is done")


def generate_faq():
    """
    Generate faq page
    """
    logging.info("Start Generating faq...")

    faq_path = "data/faq"
    faqs = []
    tags_registry = {}
    ensure_output_folder("faq")

    for mdfile in os.listdir(faq_path):
        faq_post_path = join(faq_path, mdfile)
        with open(faq_post_path, encoding="utf-8") as f:
            text = f.read()
        md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
        html = md.convert(text)
        metadata = md.Meta

        ensure_meta(["slug", "title", "tags"], metadata, faq_post_path)

        title = metadata["title"][0]
        tags = metadata["tags"]
        slug = metadata["slug"][0]
        validate_slug(slug, faq_post_path)

        content = html

        faq = {"title": title, "tags": tags, "slug": slug, "content": content}
        faqs.append(faq)

        # faq/some-question
        ensure_output_folder(join("faq", slug))
        context.update({"faq": faq})
        generate(
            "faq/post.html",
            join(settings.OUTPUT_FOLDER, "faq", slug, "index.html"),
            **context,
        )
        logging.info("Generating faq/%s...", slug)

        classify_by_tag(tags, tags_registry, faq)

    context.update({"faqs": faqs})
    generate(
        "faq/index.html", join(settings.OUTPUT_FOLDER, "faq", "index.html"), **context
    )
    logging.info("Generating faq/index.html...")
    ensure_output_folder(join("faq", "tag"))
    for tag, faqs in tags_registry.items():
        # /faq/tag/api
        context.update({"tag_name": tag, "faqs": faqs})
        ensure_output_folder(join("faq", "tag", tag))
        generate(
            "faq/tag.html",
            join(settings.OUTPUT_FOLDER, "faq", "tag", tag, "index.html"),
            **context,
        )
        logging.info("Generating faq/tag/%s/index.html...", tag)
    logging.info("Generating faq is done")


def generate_menu_pages(args):
    """
    Generate menu pages
    """
    # excluding blog post
    logging.info("Start Generating menu pages...")

    generate("index.html", join(settings.OUTPUT_FOLDER, "index.html"), **context)
    context.update({"path": "../"})

    logging.info("Generating index.html...")

    ensure_output_folder("translations")

    # If --with-trans-calc is received
    # calculated translation progress percent
    trans_progress = None
    if len(args) > 1 and args[1] == "--with-trans-calc":
        trans_progress = get_translation_data()
        langs = ', '.join(trans_progress.keys())

        logging.info("Obtaining translation information...")
        logging.info("> Detected languages: %s", langs)

    generate(
        "translations.html",
        join(settings.OUTPUT_FOLDER, "translations", "index.html"),
        trans_progress=trans_progress,
        **context,
    )
    logging.info("Generating translations.html...")

    ensure_output_folder("pallets-eco")
    generate(
        "pallets-eco.html",
        join(settings.OUTPUT_FOLDER, "pallets-eco", "index.html"),
        **context,
    )
    logging.info("Generating pallets-eco.html...")

    ensure_output_folder("join")
    generate("join.html", join(settings.OUTPUT_FOLDER, "join", "index.html"), **context)
    logging.info("Generating join.html...")

    ensure_output_folder("members")
    generate(
        "members.html", join(settings.OUTPUT_FOLDER, "members", "index.html"), **context
    )
    logging.info("Generating members.html...")

    ensure_output_folder("aim")
    generate("aim.html", join(settings.OUTPUT_FOLDER, "aim", "index.html"), **context)
    logging.info("Generating aim.html...")

    logging.info("Generating menu pages done")


def main(args):
    """
    Main function
    """
    def gen():
        ensure_exist()
        generate_menu_pages(args)  # args is for detect --with-trans-calc
        generate_profiles()
        generate_blog_posts()
        generate_resources()
        generate_faq()
        logging.info("generated folders: %s files: %s", FOLDER_COUNT, FILE_COUNT)

    if len(args) > 1 and args[1] == "--server":
        _app = Flask(__name__)

        # remember to use DEBUG mode for templates auto reload
        # https://github.com/lepture/python-livereload/issues/144
        _app.debug = True
        server = Server(_app.wsgi_app)

        # run a shell command
        # server.watch('.', 'make static')

        # run a function

        server.watch(".", gen, delay=5)
        server.watch("*.py")

        # output stdout into a file
        # server.watch('style.less', shell('lessc style.less', output='style.css'))

        server.serve()
    elif len(args) > 1 and args[1] == "--manage":
        _app.run()
    else:
        gen()


if __name__ == "__main__":
    main(sys.argv)
