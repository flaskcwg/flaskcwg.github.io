import os
import shutil

import markdown

from settings import INFO


class AuthorNotFound(Exception):
    def __init__(self, author, message="Author not found"):
        self.author = author
        self.message = f"{message}: {author}"
        super().__init__(self.message)


def get_posts():
    """Get blog and faq post"""
    blogs_dir = os.listdir("data/blog")
    faqs = os.listdir("data/faq")

    blogs = []
    for category in blogs_dir:
        bposts = os.listdir(os.path.join("data", "blog", category))
        for post in bposts:
            blogs.append([post, category])

    data = {"blogs": blogs, "faqs": faqs}

    return data


def delete_post(filePath, docs_dir):
    """Delete post .md file and rendered files in docs"""
    # First, delete main .md file (in data folder)
    os.remove(filePath)

    # Second, delete folder from docs folder
    shutil.rmtree(os.path.join("docs", docs_dir, ntpath.basename(filePath)[:-3]))


def format_authors_tags(items):
    """Format authors and tags to be compatible with Markdown metadata"""
    s = ""
    count = 0
    for item in items:
        count += 1
        if count > 1:
            # More than one author
            s += f"    {item}\n"
        else:
            s += f"{item}\n"

    return s.strip()


def get_comma_separated(string):
    """Get items in comma separated string and clean whitespaces"""
    result = [x.strip() for x in string.split(",")]
    return result


def get_md_template(post_type):
    """Return given template content"""
    with open(f"manager_app/templates/post.{post_type}.md") as f:
        content = f.read()
        return content


def ensure_authors(authors):
    """Verify if given authors are valid flaskcwg members"""
    for author in authors:
        if author not in info["profiles"]:
            raise AuthorNotFound(author)


def get_file_body(file_lines):
    """Get body of file content without metadata"""
    indicestoremove = []
    for n, line in enumerate(file_lines):
        indicestoremove.append(n)
        if "slug:" in line:
            break

    for index in sorted(indicestoremove, reverse=True):
        file_lines.pop(index)

    body = "".join(file_lines)
    return body


def parse_file(file_path):
    """Open, get and return conntent of given file"""
    with open(file_path, encoding="utf-8") as f:
        text = f.read()
    with open(file_path, encoding="utf-8") as f2:
        lines = f2.readlines()

    md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
    md.convert(text)
    metadata = md.Meta

    body = get_file_body(lines)

    return [body, metadata]


def save_md_file(post_type, data):
    """Save post to respective category (blog, faq)"""
    template = get_md_template(post_type)
    slug = data["slug"]

    if post_type == "blog":
        category = data["category"]
        post = template.format(
            data["title"],
            data["summary"],
            format_authors_tags(data["authors"]),
            data["date"],
            format_authors_tags(data["tags"]),
            slug,
            data["post_content"],
        )

        with open(f"data/blog/{category}/{slug}.md", "w") as f:
            f.write(post)
    else:
        post = template.format(
            data["title"], format_authors_tags(data["tags"]), slug, data["post_content"]
        )

        with open(f"data/faq/{slug}.md", "w") as f:
            f.write(post)
