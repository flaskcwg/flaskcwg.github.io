"""
This file is responsible for building the site
"""

import os
import re
import sys
import datetime
import logging
from functools import wraps
from os.path import join

import markdown
import validators
from flask import Flask
from livereload import Server

from jamstack.api.template import base_context, generate as generate_
import settings
from weblate import fetch_weblate_languages
import pretty_errors

# Global Counters
FOLDER_COUNT = 0
FILE_COUNT = 0

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

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

# Utility Decorators
def count_calls(counter_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            globals()[counter_name] += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

@count_calls("FOLDER_COUNT")
def ensure_output_folder(path):
    """Ensures the existence of the given path in the output directory"""
    if path == settings.OUTPUT_FOLDER:
        full_path = settings.OUTPUT_FOLDER  # Evitar la duplicación
    else:
        full_path = join(settings.OUTPUT_FOLDER, path)  # Agregar ruta relativa

    os.makedirs(full_path, exist_ok=True)

@count_calls("FILE_COUNT")
def generate(*args, **kwargs):
    """Wraps the generate_ function"""
    generate_(*args, **kwargs)

# Context Configuration
context = base_context()
context.update({
    "info": settings.INFO,
    "path": "/",
    "profile_url": lambda path, user: f"{path}u/{user}",
    "info_to_html": lambda bio: " ".join(f"<br/>" if not l.strip() else l for l in bio),
    "volunteers": settings.VOLUNTEERS_DESCS,
})

# Custom Exceptions
class InvalidSlug(Exception):
    def __init__(self, slug, filepath, message="Invalid slug"):
        super().__init__(f"{filepath}: {message}: {slug}")

class AuthorNotFound(Exception):
    def __init__(self, author, filepath, message="Author's GitHub handle not found"):
        super().__init__(f"{filepath}: {message}: {author}")

# Validation Functions
def valid_date_str(datestr):
    """Validates the date format in Markdown files"""
    pattern = r"^[a-zA-Z]+ (\d{1,2}), (\d{4})$"
    if not re.fullmatch(pattern, datestr):
        return False
    month, day = re.findall(r"[a-zA-Z]+|\d{1,2}", datestr)
    return month.lower() in [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ] and 1 <= int(day) <= 31

def validate_slug(slug, filepath):
    """Validates the given slug"""
    if not validators.slug(slug):
        raise InvalidSlug(slug, filepath)

# Core Functions
def generate_profiles():
    """Generates profile pages"""
    logging.info("Starting Profile generation...")
    profiles = settings.INFO["profiles"]
    ensure_output_folder("u")
    
    for username, data in profiles.items():
        context.update({
            "github_username": username,
            "data": data,
            "path": "../" * 2,
            "volunteers": settings.VOLUNTEERS_DESCS,
        })
        ensure_output_folder(f"u/{username}")
        generate("profile.html", join(settings.OUTPUT_FOLDER, "u", username, "index.html"), **context)
        logging.debug("Profile generated: %s", username)

    logging.info("Profile generation completed. Total profiles: %d", len(profiles))

def generate_blog_posts():
    """Generates blog posts and related pages"""
    logging.info("Starting Blog generation...")
    posts = []
    
    # Aquí asumimos que los posts están organizados en categorías dentro de data/blog
    blog_data = "data/blog"

    for category in settings.BLOG_CATEGORIES:
        category_path = join(blog_data, category)
        for mdfile in os.listdir(category_path):
            blog_post_path = join(category_path, mdfile)
            with open(blog_post_path, encoding="utf-8") as f:
                text = f.read()
            md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
            html = md.convert(text)
            metadata = md.Meta
            
            slug = metadata["slug"][0]
            ensure_output_folder(f"b/{slug}")
            
            post = {key: metadata[key][0] for key in ["slug", "title", "summary"]}
            post.update({"content": html, "category": category, "tags": metadata["tags"], "date": metadata["date"][0]})
            posts.append(post)
            
            context.update({"post": post, "path": "../" * 2})
            generate(
                "blog/post.html",
                join(settings.OUTPUT_FOLDER, "b", slug, "index.html"),
                **context
            )
            logging.debug("Generated blog post: %s", slug)

    # Generar el archivo blog/index.html principal
    ensure_output_folder("blog")
    posts.sort(key=lambda x: datetime.datetime.strptime(x["date"], "%B %d, %Y"))
    context.update({"posts": posts})
    generate(
        "blog/index.html", join(settings.OUTPUT_FOLDER, "blog", "index.html"), **context
    )
    logging.info("Blog generated successfully.")

def generate_faq():
    """Generates FAQ pages"""
    logging.info("Starting FAQ generation...")
    faq_path = "data/faq"
    faqs = []
    ensure_output_folder("faq")

    for mdfile in os.listdir(faq_path):
        faq_post_path = join(faq_path, mdfile)
        with open(faq_post_path, encoding="utf-8") as f:
            text = f.read()
        md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
        content = md.convert(text)
        meta = md.Meta
        
        slug = meta["slug"][0]
        validate_slug(slug, faq_post_path)
        
        faq = {key: meta[key][0] for key in ["slug", "title"]}
        faq.update({"content": content})
        faqs.append(faq)
        
        ensure_output_folder(join("faq", slug))
        context.update({"faq": faq})
        generate("faq/post.html", join(settings.OUTPUT_FOLDER, "faq", slug, "index.html"), **context)
        logging.debug("FAQ generated: %s", slug)

    context.update({"faqs": faqs})
    generate("faq/index.html", join(settings.OUTPUT_FOLDER, "faq", "index.html"), **context)
    logging.info("FAQ generation completed. Total FAQs: %d", len(faqs))

def generate_resources():
    """Generates the resources page"""
    logging.info("Starting Resources generation...")
    resources = settings.INFO["resources"]
    ensure_output_folder("resources")
    
    # Genera el archivo correcto resources/index.html
    generate(
        "resources/index.html",  # Ahora estamos generando resources/index.html
        join(settings.OUTPUT_FOLDER, "resources", "index.html"),
        **context
    )
    logging.info("Resources generated successfully.")

    # Additional logic for resource categories and tags
    tags_registry = {}
    for resource in resources:
        current_resource = resources[resource]["posts"]
        ensure_output_folder(join("resources", "c", resource))
        context.update({
            "resource_name": resource,
            "current_resource": current_resource,
            "path": "../" * 3,
        })
        generate(
            "resources/category.html",
            join(settings.OUTPUT_FOLDER, "resources", "c", resource, "index.html"),
            **context
        )
        logging.debug("Resource category page generated: %s", resource)

        for project in current_resource:
            tags = project["tags"]
            classify_by_tag(tags, tags_registry, project)

    # Generate tag pages
    ensure_output_folder(join("resources", "tag"))
    for tag, projects in tags_registry.items():
        ensure_output_folder(join("resources", "tag", tag))
        context.update({"tag": tag, "projects": projects, "path": "../" * 3})
        generate(
            "resources/tag.html",
            join(settings.OUTPUT_FOLDER, "resources", "tag", tag, "index.html"),
            **context
        )
        logging.debug("Resource tag page generated: %s", tag)

    logging.info("Resources generation completed.")

def generate_translations():
    """Generates the translations page"""
    logging.info("Fetching translation data...")
    translation_data = fetch_weblate_languages("flask")
    total_languages = len(translation_data)

    logging.info("Detected %d languages.", total_languages)

    generate(
        "translations.html",
        join(settings.OUTPUT_FOLDER, "translations", "index.html"),
        translations=translation_data,
        **context,
    )
    logging.info("Translations generated successfully.")

def generate_index():
    """Generates the main index.html"""
    logging.info("Generating Main index.html...")
    generate("index.html", join(settings.OUTPUT_FOLDER, "index.html"), **context)
    logging.info("Main index.html generated successfully.")

def generate_menu_pages():
    """Generates static menu pages"""
    logging.info("Generating menu pages...")
    menu_pages = ["join", "members", "aim", "translations", "pallets-eco", "resources", "blog"]
    
    # Aseguramos de generar los archivos correctos para resources y blog
    for page in menu_pages:
        ensure_output_folder(page)
        if page == "resources" or page == "blog":
            # Generamos <page>/index.html
            generate(f"{page}/index.html", join(settings.OUTPUT_FOLDER, page, "index.html"), **context)
            logging.debug(f"Generated {page}/index.html")
        else:
            # Para las demás páginas del menú
            generate(f"{page}.html", join(settings.OUTPUT_FOLDER, page, "index.html"), **context)
            logging.debug("Generated %s/index.html", page)
    
    logging.info("Menu page generation completed. Total pages: %d", len(menu_pages))


def build_site():
    """Orchestrates the site-building process."""
    ensure_output_folder(settings.OUTPUT_FOLDER)
    generate_index()
    generate_menu_pages()
    generate_profiles()
    generate_blog_posts()
    generate_resources()
    generate_faq()
    generate_translations()


def main():
    """Main entry point for the site-building script."""
    build_site()


if __name__ == "__main__":
    main()
