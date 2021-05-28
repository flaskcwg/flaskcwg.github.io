import sys
import os
from os.path import join
import markdown
import datetime

import settings
from flask import Flask
from jamstack.api.template import base_context
from jamstack.api.template import generate as generate_
from livereload import Server
import validators
from functools import wraps

folder_count = 0
file_count = 0


def count_folders(function):
    """Returns number of times any function with this decorator is called
    """

    @wraps(function)
    def increase_count(*args, **kwargs):
        global folder_count
        folder_count += 1
        return function(*args, **kwargs)

    return increase_count


def count_files(function):
    """Returns number of times any function with this decorator is called
    """

    @wraps(function)
    def increase_count(*args, **kwargs):
        global file_count
        file_count += 1
        return function(*args, **kwargs)

    return increase_count


# path is the path to main page and is required on every page


@count_files
def generate(*args, **kwargs):
    generate_(*args, **kwargs)


def profile_url(path, github_username):
    return "{}u/{}".format(path, github_username)


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
    """May 19, 2021
    TODO: switch to regex
    """
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
    if (datestr.count(" ") == 2) and (datestr.count(",") == 1):
        month = datestr.split(" ")[0]
        if month.casefold() not in months:
            return False
        year = datestr.split(" ")[2]
        if not year.isdigit():
            return False
        day = datestr.split(" ")[1].strip(",")
        if (not day.isdigit()) and (not (1 <= int(day) <= 31)):
            return False
    else:
        return False
    return True


context = base_context()
context.update(
    {
        "info": settings.info,
        "path": "/",
        "profile_url": profile_url,
        "info_to_html": info_to_html,
    }
)


class InvalidSlug(Exception):
    def __init__(self, slug, filepath, message="Invalid slug"):
        self.slug = slug
        self.filepath = filepath
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.filepath}: {self.message}: {self.slug}"


class AuthorNotFound(Exception):
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
    if not os.path.exists(join(settings.OUTPUT_FOLDER, path)):
        os.mkdir(join(settings.OUTPUT_FOLDER, path))


def ensure_exist():
    if not os.path.exists(settings.OUTPUT_FOLDER):
        os.mkdir(settings.OUTPUT_FOLDER)


def ensure_meta(taglist, metadata, document_path):
    to_ensure = taglist
    for meta in to_ensure:
        if meta not in metadata:
            print(
                "Missing meta attribute:",
                "'{}'".format(meta),
                "in path:",
                document_path,
            )
            sys.exit()


def ensure_authors(authors, filepath):
    for author in authors:
        if author not in context["info"]["profiles"]:
            raise AuthorNotFound(author, filepath)


def is_valid_slug(slugstr):
    if not validators.slug(slugstr):
        return False
    return True


def validate_slug(slug, filepath):
    if not is_valid_slug(slug):
        raise InvalidSlug(slug, filepath)


def generate_profiles():
    profiles = settings.info["profiles"]
    ensure_output_folder("u")
    for github_username in profiles:
        context.update(
            {
                "github_username": github_username,
                "data": profiles[github_username],
                "path": "../" * 2,
            }
        )
        ensure_output_folder("u/{}".format(github_username))

        generate(
            "profile.html",
            join(
                settings.OUTPUT_FOLDER, "u", "{}".format(github_username), "index.html"
            ),
            **context,
        )


def add_to_registry(tag, tags_registry, dict_object):
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
    posts = []
    blog_data = "data/blog"

    # n**2 solution
    for category in settings.BLOG_CATEGORIES:
        category_path = join(blog_data, category)
        # html = markdown.markdown(md, extensions=extensions, output_format='html5')
        for mdfile in os.listdir(category_path):
            blog_post_path = join(category_path, mdfile)
            with open(blog_post_path) as f:
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
            ensure_output_folder("b/{}".format(slug))

            ensure_authors(authors, blog_post_path)

            raw_date = metadata["date"][0]
            if valid_date_str(raw_date):
                date = raw_date
            else:
                print(
                    "Date '{date}' should be in the format 'May 19, 2021' in file '{mdfile}'".format(
                        date=raw_date, mdfile=mdfile
                    )
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

    # Blog post main page
    ensure_output_folder("blog")
    posts.sort(
        key=lambda x: datetime.datetime.strptime(x["date"], "%B %d, %Y")
    )  # May 19, 2021
    context.update({"posts": posts})
    generate(
        "blog/index.html", join(settings.OUTPUT_FOLDER, "blog", "index.html"), **context
    )

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
    for category in categories_registry:
        context.update(
            {
                "category": category,
                "posts": categories_registry[category],
                "path": "../" * 2,
            }
        )
        generate(
            "category.html",
            join(settings.OUTPUT_FOLDER, "category", category, "index.html"),
            **context,
        )

    for tag in tags_registry:
        context.update({"tag": tag, "posts": tags_registry[tag], "path": "../" * 2})
        generate(
            "blog/tag.html",
            join(settings.OUTPUT_FOLDER, "tag", tag, "index.html"),
            **context,
        )


def generate_resources():
    resources = settings.info["resources"]

    # /resources
    ensure_output_folder("resources")
    ensure_output_folder("resources/c")
    generate(
        "resources/index.html",
        join(settings.OUTPUT_FOLDER, "resources", "index.html"),
        **context,
    )

    tags_registry = {}
    # /resources/c/api/ # for category. category name cannot be tag
    for resource in resources:
        current_resource = resources[resource]
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

        for project in current_resource:
            tags = project["tags"]
            classify_by_tag(tags, tags_registry, project)

    # /resources/tag/asgi
    ensure_output_folder(join("resources", "tag"))
    for tag in tags_registry:
        ensure_output_folder(join("resources", "tag", tag))
        context.update({"tag": tag, "projects": tags_registry[tag], "path": "../" * 3})
        generate(
            "resources/tag.html",
            join(settings.OUTPUT_FOLDER, "resources", "tag", tag, "index.html"),
            **context,
        )


def generate_faq():
    faq_path = "data/faq"
    faqs = []
    tags_registry = {}
    ensure_output_folder("faq")

    for mdfile in os.listdir(faq_path):
        faq_post_path = join(faq_path, mdfile)
        with open(faq_post_path) as f:
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

        classify_by_tag(tags, tags_registry, faq)

    context.update({"faqs": faqs})
    generate(
        "faq/index.html", join(settings.OUTPUT_FOLDER, "faq", "index.html"), **context
    )

    ensure_output_folder(join("faq", "tag"))
    for tag in tags_registry:
        # /faq/tag/api
        context.update({"tag_name": tag, "faqs": tags_registry[tag]})
        ensure_output_folder(join("faq", "tag", tag))
        generate(
            "faq/tag.html",
            join(settings.OUTPUT_FOLDER, "faq", "tag", tag, "index.html"),
            **context,
        )


def generate_menu_pages():
    # excluding blog post
    generate("index.html", join(settings.OUTPUT_FOLDER, "index.html"), **context)

    context.update({"path": "../"})

    ensure_output_folder("translations")
    generate(
        "translations.html",
        join(settings.OUTPUT_FOLDER, "translations", "index.html"),
        **context,
    )

    ensure_output_folder("takeover")
    generate(
        "takeover.html",
        join(settings.OUTPUT_FOLDER, "takeover", "index.html"),
        **context,
    )

    ensure_output_folder("join")
    generate("join.html", join(settings.OUTPUT_FOLDER, "join", "index.html"), **context)

    ensure_output_folder("members")
    generate(
        "members.html", join(settings.OUTPUT_FOLDER, "members", "index.html"), **context
    )

    ensure_output_folder("aim")
    generate("aim.html", join(settings.OUTPUT_FOLDER, "aim", "index.html"), **context)


def main(args):
    def gen():
        ensure_exist()
        generate_menu_pages()
        generate_profiles()
        generate_blog_posts()
        generate_resources()
        generate_faq()
        print(f"generated folders: {folder_count} files: {file_count}")

    if len(args) > 1 and args[1] == "--server":
        app = Flask(__name__)

        # remember to use DEBUG mode for templates auto reload
        # https://github.com/lepture/python-livereload/issues/144
        app.debug = True
        server = Server(app.wsgi_app)

        # run a shell command
        # server.watch('.', 'make static')

        # run a function

        server.watch(".", gen, delay=5)
        server.watch("*.py")

        # output stdout into a file
        # server.watch('style.less', shell('lessc style.less', output='style.css'))

        server.serve()
    else:
        gen()


if __name__ == "__main__":
    main(sys.argv)
