import os
from github import Github
import requests
import jinja2

TOKEN = os.environ["GH_TOKEN"]
ORG = "daily-ultimate-game"
TEMPLATE_MARKER = "setting/game.json"
DEFAULT_BRANCH = "main"
DEFAULT_IMAGE = "https://placehold.co/300x200?text=No+Image"

g = Github(TOKEN)
org = g.get_organization(ORG)
repos = org.get_repos()

games = []
for repo in repos:
    try:
        file = repo.get_contents(TEMPLATE_MARKER)
        meta = requests.get(file.download_url).json()
        meta["repo_url"] = f"https://github.com/{ORG}/{repo.name}"

        cover = meta.get("cover_image", "")
        if cover and not cover.startswith("http"):
            # Build raw.github link for image in the setting subfolder
            meta["cover_image"] = f"https://raw.githubusercontent.com/{ORG}/{repo.name}/{DEFAULT_BRANCH}/setting/{cover}"
        elif not cover:
            meta["cover_image"] = DEFAULT_IMAGE
        games.append(meta)
    except Exception:
        continue

# Fancier Jinja2 template for HTML
template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>🎮 Ultimate Game Gallery</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
<style>
body {
    background: #181c24;
    min-height: 100vh;
    font-family: 'Montserrat', 'Segoe UI', 'Roboto', sans-serif;
    color: #fff;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    position: relative;
}
.header {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    font-size: 2.8rem;
    font-family: 'Orbitron', 'Montserrat', sans-serif;
    font-weight: bold;
    letter-spacing: 2.5px;
    background: linear-gradient(90deg,#f7971e,#ffd200,#21d4fd,#b721ff,#ff006a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-move 3s linear infinite alternate;
}
@keyframes gradient-move {
    0% { background-position: 0%;}
    100% { background-position: 100%;}
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit,minmax(320px,1fr));
    gap: 2.2rem;
    padding: 2.5rem 2vw 3rem 2vw;
    z-index: 1;
    position: relative;
}
.card {
    background: rgba(30, 30, 40, 0.98);
    border-radius: 22px;
    box-shadow: 0 4px 32px 0 rgba(0,0,0,0.55), 0 0 0 2px #21d4fd33;
    overflow: hidden;
    transition: transform 0.22s, box-shadow 0.22s, border 0.22s;
    position: relative;
    border: 2px solid transparent;
    cursor: pointer;
}
.card:hover {
    transform: translateY(-10px) scale(1.035) rotate(-1deg);
    box-shadow: 0 8px 40px 0 #21d4fd55, 0 0 0 4px #ffd20055;
    border: 2px solid #ffd200;
    z-index: 2;
}
.card img {
    width: 100%;
    height: 190px;
    object-fit: cover;
    display: block;
    border-bottom: 2px solid #21d4fd55;
    background: #232526;
    transition: filter 0.2s;
}
.card:hover img {
    filter: brightness(1.08) saturate(1.2) drop-shadow(0 0 12px #ffd20088);
}
.card-content {
    padding: 1.6rem 1.3rem 1.2rem 1.3rem;
}
.card-title {
    font-size: 1.35rem;
    font-family: 'Orbitron', 'Montserrat', sans-serif;
    font-weight: bold;
    margin-bottom: 0.7rem;
    color: #ffd200;
    letter-spacing: 1.2px;
    text-shadow: 0 2px 8px #23252688;
}
.card-desc {
    font-size: 1.04rem;
    color: #e3e3e3;
    margin-bottom: 1.3rem;
    min-height: 48px;
    font-family: 'Montserrat', sans-serif;
}
.page-link {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    background: linear-gradient(90deg,#21d4fd,#b721ff,#ff006a);
    color: #fff;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 700;
    letter-spacing: 1.1px;
    font-family: 'Montserrat', 'Orbitron', sans-serif;
    transition: background 0.18s, box-shadow 0.18s;
    box-shadow: 0 2px 12px rgba(33, 212, 253, 0.13);
    border: none;
    outline: none;
    font-size: 1.05rem;
}
.page-link:hover {
    background: linear-gradient(90deg,#b721ff,#21d4fd,#ffd200);
    box-shadow: 0 4px 18px #ffd20055;
    color: #232526;
}
@media (max-width: 700px) {
    .header { font-size: 1.5rem; }
    .card img { height: 110px; }
    .card-content { padding: 1rem; }
    .grid { gap: 1.2rem; padding: 1.2rem 1vw 2rem 1vw;}
}
.particles {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 0;
}
</style>
</head>
<body>
<canvas class="particles"></canvas>
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
<script>
// Simple animated particles background
const canvas = document.querySelector('.particles');
const ctx = canvas.getContext('2d');
let w = window.innerWidth, h = window.innerHeight;
canvas.width = w; canvas.height = h;
window.addEventListener('resize', () => {
    w = window.innerWidth; h = window.innerHeight;
    canvas.width = w; canvas.height = h;
});
const particles = Array.from({length: 38}, () => ({
    x: Math.random()*w, y: Math.random()*h,
    r: 1.5+Math.random()*2.5,
    dx: -0.5+Math.random(), dy: -0.5+Math.random(),
    c: `hsla(${Math.random()*360},90%,60%,0.18)`
}));
function draw() {
    ctx.clearRect(0,0,w,h);
    for(const p of particles) {
        ctx.beginPath();
        ctx.arc(p.x,p.y,p.r,0,2*Math.PI);
        ctx.fillStyle = p.c;
        ctx.shadowColor = p.c;
        ctx.shadowBlur = 8;
        ctx.fill();
        p.x += p.dx; p.y += p.dy;
        if(p.x<0||p.x>w) p.dx*=-1;
        if(p.y<0||p.y>h) p.dy*=-1;
    }
    requestAnimationFrame(draw);
}
draw();
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(jinja2.Template(template).render(games=games))
