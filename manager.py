import datetime
import ntpath
import shutil

import markdown
from flask import Flask, redirect, render_template, request, url_for

from manager_utils import *
from settings import BLOG_CATEGORIES

app = Flask(
    __name__,
    template_folder="manager_app/templates",
    static_folder="manager_app/static",
)
app.config.update(
    DEBUG=True, SECRET_KEY=b"sC&wJQ35C3jR", SQLALCHEMY_TRACK_MODIFICATIONS=False
)


@app.route("/")
def index():
    posts = get_posts()
    resources = INFO["resources"]
    current_day = datetime.date.today()
    today = datetime.date.strftime(current_day, "%B %d, %Y")

    return render_template(
        "index.html",
        today=today,
        b_categories=BLOG_CATEGORIES,
        posts=posts,
        resources=resources,
    )


@app.route("/save_post", methods=["POST"])
def save_post():
    # Validate empty fields?
    post_type = request.form["post-type"]
    if request.form["post-type"] == "blog":
        data = {
            "title": request.form["b_title"],
            "summary": request.form["b_summ"],
            "authors": get_comma_separated(request.form["b_authors"]),
            "date": request.form["b_date"],
            "tags": get_comma_separated(request.form["b_tags"]),
            "slug": request.form["b_slug"],
            "post_content": request.form["post_content"],
            "category": request.form["b_category"],
        }

        ensure_authors(data["authors"])
        save_md_file(post_type, data)

    else:
        data = {
            "slug": request.form["f_slug"],
            "tags": get_comma_separated(request.form["f_tags"]),
            "title": request.form["f_title"],
            "post_content": request.form["post_content"],
        }
        save_md_file(post_type, data)

    return 'Post saved! Remember re-build the site to see the changes. <a href="/">Return</a>'


@app.route("/action/<string:ptype>/<string:option>/<string:post>", methods=["GET"])
def postman(ptype, option, post):
    if option == "edit":
        posts = get_posts()

        if ptype == "blog":
            filename, category = post.split("@")
            blog_post_path = os.path.join("data", "blog", category, filename)

            body, metadata = parse_file(blog_post_path)

            postdata = {
                "title": metadata["title"][0],
                "summary": metadata["summary"][0],
                "authors": ",".join(metadata["authors"]),
                "date": metadata["date"][0],
                "tags": ",".join(metadata["tags"]),
                "slug": metadata["slug"][0],
                "category": category,
                "content": body,
            }

            return render_template(
                "edit_page.html", postdata=postdata, posts=posts, edit_type="blog"
            )
        else:
            faq_post_path = os.path.join("data", "faq", post)
            body, metadata = parse_file(faq_post_path)

            postdata = {
                "title": metadata["title"][0],
                "tags": ",".join(metadata["tags"]),
                "slug": metadata["slug"][0],
                "content": body,
            }

            return render_template(
                "edit_page.html", postdata=postdata, posts=posts, edit_type="faq"
            )

    else:
        if ptype == "blog":
            filename, category = post.split("@")
            delete_post(os.path.join("data", "blog", category, filename), docs_dir="b")
        else:
            delete_post(os.path.join("data", "faq", post), docs_dir="faq")

        return 'Post deleted! Do not forget to rebuild the site to remove the remaining references. <a href="/">Return</a>'


if __name__ == "__main__":
    app.run()
