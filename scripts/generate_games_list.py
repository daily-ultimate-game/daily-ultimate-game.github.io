import os
from github import Github
import requests
import jinja2

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG = "daily-ultimate-game"
TEMPLATE_MARKER = "game.json"

g = Github(GITHUB_TOKEN)
org = g.get_organization(ORG)
repos = org.get_repos()

games = []
for repo in repos:
    try:
        file = repo.get_contents(TEMPLATE_MARKER)
        metadata = requests.get(file.download_url).json()
        games.append(metadata)
    except Exception:
        continue

# Render HTML
template = """<html><body>
<h1>All Games</h1>
<ul>
{% for game in games %}
<li>
  <img src="{{game.cover_image}}" height="80"/> <b>{{game.title}}</b> - {{game.description}}
  [<a href="https://github.com/{{game.repo}}">Repo</a>]
</li>
{% endfor %}
</ul>
</body></html>
"""

with open("games.html", "w") as f:
    f.write(jinja2.Template(template).render(games=games))