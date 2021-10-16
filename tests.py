import pprint

'''
import html2markdown
import html2text
import markdown
import tomd
from markdownify import markdownify

with open("data/faq/migrate-doc-translation-repo-to-flaskcwg-org.md", encoding="utf-8") as f:
    lines = f.readlines()

lines = [line for line in lines]
print(lines)
'''
#print(''.join(lines))
s = ['title: Migrate doc translation repo to FlaskCWG org\n', 'tags: migration\n', '    flask\n', '    repo\n', 'slug: migrate-doc-translation-repo-to-flaskcwg-org\n', '\n', '> **Note**: In order to transfer ownership you must be a member of the organization.\n', '\n', '\n', '\n', '1. Go to repo **Settings**\n', '\n', '2. Scroll to the bottom of the page, under **Danger Zone**\n', '\n', '3. In the **Transfer ownership** section press the **Transfer** button\n', '\n', '4. In the pop-up window, in the available field look for the organization and select it. Below you will be asked to confirm the name of the repository\n', '\n', '5. Press **I understand, transfer this ownership**\n', '\n', '\n', '\n', 'After the transfer process you will lose the ability to make direct modifications to the repository so you will have to request to increase your permissions on the repository, this clearly only applies to Translation Coordinators.\n']

#s = [x.replace("\n","") for x in s]
#print("".join(s).replace("\n\n", "\n"))
for x in s:
    print(x)
