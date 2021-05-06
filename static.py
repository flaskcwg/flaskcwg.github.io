# https://github.com/pymug/website-AV19-AV20

import sys
from os.path import join

import settings
from flask import Flask
from jamstack.api.template import base_context, generate
from livereload import Server

context = base_context()
context.update({
    "info": settings.info
})


def main(args):
    def gen():
        generate('index.html', join(
            settings.OUTPUT_FOLDER, 'index.html'), **context)
        generate('translations.html', join(
            settings.OUTPUT_FOLDER, 'translations.html'), **context)

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
