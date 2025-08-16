import os
from github import Github
import requests
import jinja2

TOKEN = os.environ["GH_TOKEN"]
ORG = "daily-ultimate-game"
TEMPLATE_MARKER = "game.json"

g = Github(TOKEN)
org = g.get_organization(ORG)
repos = org.get_repos()

games = []
for repo in repos:
    try:
        file = repo.get_contents(TEMPLATE_MARKER)
        meta = requests.get(file.download_url).json()
        # Add repo URL and fallback image if missing
        meta["repo_url"] = f"https://github.com/{ORG}/{repo.name}"
        meta["cover_image"] = meta.get("cover_image", "https://placehold.co/300x200?text=No+Image")
        games.append(meta)
    except Exception:
        continue

# Jinja2 template for fancy HTML
template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>🎮 Ultimate Game Gallery</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    background: linear-gradient(120deg, #232526, #485563);
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    color: #fff;
    margin: 0;
    padding: 0;
}
.header {
    text-align: center;
    padding: 2rem 0 1rem 0;
    font-size: 2.5rem;
    font-weight: bold;
    letter-spacing: 2px;
    background: linear-gradient(90deg,#f7971e,#ffd200,#21d4fd,#b721ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit,minmax(300px,1fr));
    gap: 2rem;
    padding: 2rem;
}
.card {
    background: rgba(30, 30, 40, 0.96);
    border-radius: 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.45);
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
}
.card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 8px 32px rgba(0,0,0,0.7);
}
.card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
}
.card-content {
    padding: 1.5rem;
}
.card-title {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 0.7rem;
    color: #ffd200;
    letter-spacing: 1px;
}
.card-desc {
    font-size: 1rem;
    color: #e3e3e3;
    margin-bottom: 1.2rem;
}
.page-link {
    display: inline-block;
    padding: 0.5rem 1.1rem;
    background: linear-gradient(90deg,#21d4fd,#b721ff);
    color: #fff;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    letter-spacing: 1px;
    transition: background 0.2s;
    box-shadow: 0 2px 8px rgba(33, 212, 253, 0.1);
}
.page-link:hover {
    background: linear-gradient(90deg,#b721ff,#21d4fd);
}
@media (max-width: 600px) {
    .header { font-size: 1.6rem; }
    .card img { height: 120px; }
    .card-content { padding: 1rem; }
}
</style>
</head>
<body>
<div class="header">🎮 Ultimate Game Gallery</div>
<div class="grid">
{% for game in games %}
    {% if game.title != "ultimate-game-template" %}
    <div class="card">
        <img src="{{ game.cover_image }}" alt="{{ game.title }} cover">
        <div class="card-content">
            <div class="card-title">{{ game.title }}</div>
            <div class="card-desc">{{ game.description }}</div>
            <a class="page-link" href="https://daily-ultimate-game.github.io/{{ game.title | replace(' ', '-') }}/" target="_blank">View Page</a>
        </div>
    </div>
    {% endif %}
{% endfor %}
</div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(jinja2.Template(template).render(games=games))
