# https://github.com/pymug/website-AV19-AV20

import sys
import os
from os.path import join

import settings
from flask import Flask
from jamstack.api.template import base_context
from jamstack.api.template import generate
from livereload import Server

context = base_context()
context.update({
    "info": settings.info,
    'path': '/'
})


def ensure_exist():
    if not os.path.exists(join(settings.OUTPUT_FOLDER, 'u')):
        os.mkdir(join(settings.OUTPUT_FOLDER, 'u'))


def generate_profiles():
    profiles = settings.info['profiles']
    for github_username in profiles:
        context.update({
            'github_username': github_username,
            'data': profiles[github_username],
            'path': '../'
            })
        generate('profile.html', join(
            settings.OUTPUT_FOLDER, 'u', '{}.html'.format(github_username)), **context)


def generate_menu_pages():
    generate('index.html', join(
        settings.OUTPUT_FOLDER, 'index.html'), **context)
    generate('translations.html', join(
        settings.OUTPUT_FOLDER, 'translations.html'), **context)
    generate('takeover.html', join(
        settings.OUTPUT_FOLDER, 'takeover.html'), **context)
    generate('join.html', join(
        settings.OUTPUT_FOLDER, 'join.html'), **context)
    generate('blog.html', join(
        settings.OUTPUT_FOLDER, 'blog.html'), **context)
    generate('members.html', join(
        settings.OUTPUT_FOLDER, 'members.html'), **context)
    generate('aim.html', join(
        settings.OUTPUT_FOLDER, 'aim.html'), **context)


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
