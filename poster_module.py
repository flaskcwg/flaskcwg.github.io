import datetime
import os
import shutil

import ntpath
from flask import Flask, redirect, render_template, request, url_for
from settings import BLOG_CATEGORIES, info


class AuthorNotFound(Exception):
    def __init__(self, author, message="Author not found"):
        self.author = author
        self.message = f'{message}: {author}'
        super().__init__(self.message)

def get_posts():
    blogs_dir = os.listdir('data/blog')
    faqs = os.listdir('data/faq')

    blogs = []
    for category in blogs_dir:
        bposts = os.listdir(os.path.join('data', 'blog', category))
        for post in bposts:
            blogs.append([post, category])

    data = {'blogs':blogs, 'faqs':faqs}
    
    return data

def delete_post(filePath, docs_dir):
    # First, delete main .md file (in data folder)
    os.remove(filePath) 
   
    # Second, delete folder from docs folder
    shutil.rmtree(os.path.join('docs', docs_dir, ntpath.basename(filePath)[:-3]))

def format_authors_tags(items):
    '''Format authors and tags to be compatible with Markdown metadata'''
    s = ''
    count = 0
    for item in items:
        count += 1 # If more than one item, insert identation to the nexts
        if count > 1:
            s += f'    {item}\n'
        else:
            s += f'{item}\n'
    
    return s.strip()

def get_comma_separated(string):
    # Get items in comma separated string and clean whitespaces
    result = [x.strip() for x in string.split(',')]
    return result

def get_md_template(post_type):
    # Return given template content
    with open(f'poster/templates/post.{post_type}.md') as f:
        content = f.read()
        return content

def ensure_authors(authors):
    '''Verify if given authors are valid flaskcwg members'''
    for author in authors:
        if author not in info["profiles"]:
            raise AuthorNotFound(author)


def save_md_file(post_type, data):
    template = get_md_template(post_type)
    slug = data['slug']

    if post_type == 'blog':
        category = data['category']
        post = template.format(data['title'],
                               data['summary'],
                               format_authors_tags(data['authors']),
                               data['date'],
                               format_authors_tags(data['tags']),
                               slug,
                               data['post_content'])

        with open(f'data/blog/{category}/{slug}.md', 'w') as f:
            f.write(post)
    else:
        post = template.format(data['title'],
                               format_authors_tags(data['tags']),
                               slug,
                               data['post_content'])

        with open(f'data/faq/{slug}.md', 'w') as f:
            f.write(post)

app = Flask(__name__, template_folder='poster/templates', static_folder='poster/static')
app.config.update(
    DEBUG=True,
    SECRET_KEY=b'sC&wJQ35C3jR',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

@app.route("/")
def index():
    posts = get_posts()
    current_day = datetime.date.today()
    print('time', current_day)
    today = datetime.date.strftime(current_day, "%B %d, %Y")

    return render_template("index.html", today=today, b_categories=BLOG_CATEGORIES, posts=posts)

@app.route("/save_post", methods=['POST'])
def save_post():
    # Validate empty fields?
    post_type = request.form['post-type']
    if request.form['post-type'] == 'blog':
        data = {
            'title' : request.form['b_title'],
            'summary' : request.form['b_summ'],
            'authors' : get_comma_separated(request.form['b_authors']),
            'date' : request.form['b_date'],
            'tags' : get_comma_separated(request.form['b_tags']),
            'slug' : request.form['b_slug'],
            'post_content' : request.form['post_content'],
            'category' : request.form['b_category']
        }
        ensure_authors(data['authors'])
        save_md_file(post_type, data)

    else:
        data = {
            'slug' : request.form['f_slug'],
            'tags' : get_comma_separated(request.form['f_tags']),
            'title' : request.form['f_title'],
            'post_content' : request.form['post_content']
        }

        save_md_file(post_type, data)
    
    return 'Post saved! Remember re-build the site to see the changes. <a href="/">Return</a>'
    

@app.route("/action/<string:ptype>/<string:option>/<string:post>", methods=['GET'])
def postman(ptype, option, post):
    if option == 'edit':
        # Coming soon
        pass
    else:
        if ptype == 'blog':
            filename, category = post.split('@')
            delete_post(os.path.join('data', 'blog', category, filename), docs_dir='b')
        else:
            delete_post(os.path.join('data', 'faq', post), docs_dir='faq')

        return 'Post deleted! Do not forget to rebuild the site to remove the remaining references. <a href="/">Return</a>'



if __name__ == "__main__":
    app.run()
