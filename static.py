import sys
import os
from os.path import join
import markdown
import datetime

import settings
from flask import Flask
from jamstack.api.template import base_context
from jamstack.api.template import generate
from livereload import Server
import validators

# path is the path to main page and is required on every page

def profile_url(path, github_username):
    return '{}u/{}'.format(path, github_username)


def bio_to_html(biolist):
    final_list = []
    for l in biolist:
        if l.strip() == '':
            final_list.append('<br/>')
        else:
            final_list.append(l)
    return ' '.join(final_list)

def valid_date_str(datestr):
    '''May 19, 2021'''
    months = ['january', 'february', 'march', 'april',
    'may', 'june', 'july', 'august', 'september', 'october', 
    'november', 'december']
    if (
        (datestr.count(' ') == 2) and
        (datestr.count(',') == 1)
        ):
        month = datestr.split(' ')[0]
        if (month.casefold() not in months):
            return False
        year = datestr.split(' ')[2]
        if (not year.isdigit() ):
            return False
        day = datestr.split(' ')[1].strip(',')
        if (
            (not day.isdigit()) and
            (not (1 <= int(day) <= 31))
            ):
            return False
    else:
        return False
    return True


context = base_context()
context.update({
    "info": settings.info,
    'path': '/',
    'profile_url': profile_url,
    'bio_to_html': bio_to_html
})


def ensure_output_folder(path):
    if not os.path.exists(join(settings.OUTPUT_FOLDER, path)):
        os.mkdir(join(settings.OUTPUT_FOLDER, path))

def ensure_exist():
    if not os.path.exists(settings.OUTPUT_FOLDER):
        os.mkdir(settings.OUTPUT_FOLDER)


def generate_profiles():
    profiles = settings.info['profiles']
    ensure_output_folder('u')
    for github_username in profiles:
        context.update({
            'github_username': github_username,
            'data': profiles[github_username],
            'path': '../' * 2
            })
        ensure_output_folder('u/{}'.format(github_username))
        generate('profile.html', join(
            settings.OUTPUT_FOLDER, 'u', '{}'.format(github_username), 'index.html'), **context)


def generate_blog_posts():
    posts = []
    blog_data = 'data/blog'

    # n**2 solution
    for category in settings.BLOG_CATEGORIES:
        category_path = join(blog_data, category)
        # html = markdown.markdown(md, extensions=extensions, output_format='html5')
        for mdfile in os.listdir(category_path):
            blog_post_path = join(category_path, mdfile)
            with open(blog_post_path) as f:
                text = f.read()
            md = markdown.Markdown(extensions=['extra', 'smarty', 'meta'])
            html = md.convert(text)
            metadata = md.Meta

            # validating metadata
            to_ensure = ['slug', 'authors', 'date', 'title', 'summary', 'tags']
            for meta in to_ensure:
                if meta not in metadata:
                    print('Missing meta attribute:', "'{}'".format(meta), 'in blog post:', blog_post_path)
                    sys.exit()

            ensure_output_folder('b')

            slug = metadata['slug'][0]
            if (not validators.slug(slug)):
                print("Invalid slug '{slug}' for file {mdfile}".format(slug=slug, mdfile=mdfile))
                sys.exit()
            ensure_output_folder('b/{}'.format(slug))
            authors = metadata['authors']

            for author in authors:
                if author not in context['info']['profiles']:
                    print("Cannot find author '{author}' in profiles for file {mdfile}".format(author=author, mdfile=mdfile))
                    sys.exit()

            raw_date = metadata['date'][0]
            if valid_date_str(raw_date):
                date = raw_date
            else:
                print("Date '{date}' should be in the format 'May 19, 2021' in file '{mdfile}'".format(date=raw_date, mdfile=mdfile))
                sys.exit()
            title = metadata['title'][0]
            summary = metadata['summary'][0]
            tags = metadata['tags']
            post = {
                'slug': slug,
                'content': html,
                'authors': authors,
                'date': date,
                'title': title,
                'summary': summary,
                'category': category,
                'tags': tags
            }
            posts.append(post)
            context.update({
                'post': post,
                'path': '../' * 2
                })
            generate('blog_post.html', join(
                settings.OUTPUT_FOLDER, 'b', slug, 'index.html'), **context)

    # Blog post main page
    ensure_output_folder('blog')
    posts.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%B %d, %Y')) # May 19, 2021
    context.update({'posts': posts})
    generate('blog.html', join(
        settings.OUTPUT_FOLDER, 'blog', 'index.html'), **context)

    # Category & tags scouting
    # Could also be done above but cleaner code here
    ensure_output_folder('category')
    ensure_output_folder('tag')
    categories = {}
    tags_registry = {}
    for post in posts:
        category = post['category']
        tags = post['tags']

        if category not in categories:
            ensure_output_folder(join('category', category))
            categories[category] = []
            categories[category].append(post)
        else:
            categories[category].append(post)

        for tag in tags:
            if tag not in tags_registry:
                ensure_output_folder(join('tag', tag))
                tags_registry[tag] = []
                tags_registry[tag].append(post)
            else:
                tags_registry[tag].append(post)

    # Generating category pages
    for category in categories:
        context.update({
            'category': category,
            'posts': categories[category],
            'path': '../' *2
            })
        generate('category.html', join(
                    settings.OUTPUT_FOLDER, 'category', category, 'index.html'), **context)

    for tag in tags_registry:
        context.update({
            'tag': tag,
            'posts': tags_registry[tag],
            'path': '../' *2
            })
        generate('tag.html', join(
                    settings.OUTPUT_FOLDER, 'tag', tag, 'index.html'), **context)


def generate_resources():
    resources = settings.info['resources']

    # /resources
    ensure_output_folder('resources')
    ensure_output_folder('resources/c')
    generate('resources/index.html', join(
                settings.OUTPUT_FOLDER, 'resources', 'index.html'), **context)

    tags_registry = {}
    # /resources/c/api/ # for category. category name cannot be tag
    for resource in resources:
        current_resource = resources[resource]
        ensure_output_folder(join('resources', 'c', resource))
        context.update({
            'resource_name': resource,
            'current_resource': current_resource,
            'path': '../' *3
            })
        generate('resources/category.html', join(
                settings.OUTPUT_FOLDER, 'resources', 'c', resource, 'index.html'), **context)

        for project in current_resource:
            tags = project['tags']
            for tag in tags:
                if tag not in tags_registry:
                    tags_registry[tag] = []
                    tags_registry[tag].append(project)
                else:
                    tags_registry[tag].append(project)

    # /resources/tag/asgi
    ensure_output_folder(join('resources', 'tag'))
    for tag in tags_registry:
        ensure_output_folder(join('resources', 'tag', tag))
        context.update({
            'tag': tag,
            'projects': tags_registry[tag],
            'path': '../' *3
            })
        generate('resources/tag.html', join(
                    settings.OUTPUT_FOLDER, 'resources', 'tag', tag, 'index.html'), **context)


def generate_faq():
    faq_path = 'data/faq'
    faqs = []
    tags_registry = {}
    ensure_output_folder('faq')

    for mdfile in os.listdir(faq_path):
        faq_post_path = join(faq_path, mdfile)
        with open(faq_post_path) as f:
            text = f.read()
        md = markdown.Markdown(extensions=['extra', 'smarty', 'meta'])
        html = md.convert(text)
        metadata = md.Meta

        # validating metadata
        to_ensure = ['slug', 'title', 'tags']
        for meta in to_ensure:
            if meta not in metadata:
                print('Missing meta attribute:', "'{}'".format(meta), 'in blog post:', faq_post_path)
                sys.exit()

        title = metadata['title'][0]
        tags = metadata['tags']
        slug = metadata['slug'][0]
        if (not validators.slug(slug)):
            print("Invalid slug '{slug}' for file {mdfile}".format(slug=slug, mdfile=mdfile))
            sys.exit()

        content = html

        faq = {
            'title': title,
            'tags': tags,
            'slug': slug,
            'content': content
        }
        faqs.append(faq)

        # faq/some-question
        ensure_output_folder(join('faq', slug))
        context.update({
            'faq': faq
            })
        generate('faq/post.html', join(
                    settings.OUTPUT_FOLDER, 'faq', slug, 'index.html'), **context)

        for tag in tags:
            if tag not in tags_registry:
                tags_registry[tag] = []
                tags_registry[tag].append(faq)
            else:
                tags_registry[tag].append(faq)



    context.update({
        'faqs': faqs
        })
    generate('faq/index.html', join(
                    settings.OUTPUT_FOLDER, 'faq', 'index.html'), **context)

    ensure_output_folder(join('faq', 'tag'))
    for tag in tags_registry:
        # /faq/tag/api
        context.update({
            'tag_name': tag,
            'faqs': tags_registry[tag]
            })
        ensure_output_folder(join('faq', 'tag', tag))
        generate('faq/tag.html', join(
                    settings.OUTPUT_FOLDER, 'faq', 'tag', tag, 'index.html'), **context)



def generate_menu_pages():
    # excluding blog post
    generate('index.html', join(
        settings.OUTPUT_FOLDER, 'index.html'), **context)

    context.update({
            'path': '../'
            })

    ensure_output_folder('translations')
    generate('translations.html', join(
        settings.OUTPUT_FOLDER, 'translations', 'index.html'), **context)

    ensure_output_folder('takeover')
    generate('takeover.html', join(
        settings.OUTPUT_FOLDER, 'takeover', 'index.html'), **context)

    ensure_output_folder('join')
    generate('join.html', join(
        settings.OUTPUT_FOLDER, 'join', 'index.html'), **context)

    ensure_output_folder('members')
    generate('members.html', join(
        settings.OUTPUT_FOLDER, 'members', 'index.html'), **context)

    ensure_output_folder('aim')
    generate('aim.html', join(
        settings.OUTPUT_FOLDER, 'aim', 'index.html'), **context)


def main(args):
    def gen():
        ensure_exist()
        generate_menu_pages()
        generate_profiles()
        generate_blog_posts()
        generate_resources()
        generate_faq()

    if len(args) > 1 and args[1] == '--server':
        app = Flask(__name__)

        # remember to use DEBUG mode for templates auto reload
        # https://github.com/lepture/python-livereload/issues/144
        app.debug = True
        server = Server(app.wsgi_app)

        # run a shell command
        # server.watch('.', 'make static')

        # run a function

        server.watch('.', gen, delay=5)
        server.watch('*.py')

        # output stdout into a file
        # server.watch('style.less', shell('lessc style.less', output='style.css'))

        server.serve()
    else:
        gen()


if __name__ == '__main__':
    main(sys.argv)
