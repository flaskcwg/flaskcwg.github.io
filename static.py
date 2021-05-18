import sys
import os
from os.path import join

import settings
from flask import Flask
from jamstack.api.template import base_context
from jamstack.api.template import generate
from livereload import Server

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
    for github_username in profiles:
        context.update({
            'github_username': github_username,
            'data': profiles[github_username],
            'path': '../' * 2
            })
        ensure_output_folder('u')
        ensure_output_folder('u/{}'.format(github_username))
        generate('profile.html', join(
            settings.OUTPUT_FOLDER, 'u', '{}'.format(github_username), 'index.html'), **context)


def generate_menu_pages():
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

    ensure_output_folder('blog')
    generate('blog.html', join(
        settings.OUTPUT_FOLDER, 'blog', 'index.html'), **context)

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
