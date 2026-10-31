import requests, calendar, datetime, os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

USER = "Oladee24"
W, H = 1920, 1080

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "wallpaper.png")
TODO = os.path.join(BASE, "todo.txt")

BG, CARD = (15, 17, 26), (26, 30, 43)
TEXT, MUTED, ACCENT = (235, 238, 245), (130, 138, 160), (156, 175, 136)   # sage
TODO_GREEN, TODO_DONE = (120, 200, 140), (82, 122, 94)
LEVELS = [(38, 43, 60), (14, 68, 41), (0, 109, 50), (38, 166, 65), (57, 211, 83)]

def font(size, bold=False, italic=False):
    if bold and italic:
        names = ["segoeuiz.ttf", "arialbi.ttf"]
    elif bold:
        names = ["segoeuib.ttf", "arialbd.ttf"]
    elif italic:
        names = ["segoeuii.ttf", "ariali.ttf"]
    else:
        names = ["segoeui.ttf", "arial.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def card(box):
    d.rounded_rectangle(box, radius=22, fill=CARD)

def fit(text, f, max_w):
    while d.textlength(text, font=f) > max_w and len(text) > 1:
        text = text[:-2] + "…"
    return text

# ---------- GitHub numbers ----------
try:
    u = requests.get(f"https://api.github.com/users/{USER}", timeout=10).json()
    repos = requests.get(f"https://api.github.com/users/{USER}/repos?per_page=100", timeout=10).json()
    stats = [("Public repos", u["public_repos"]),
             ("Followers", u["followers"]),
             ("Following", u["following"]),
             ("Stars earned", sum(r["stargazers_count"] for r in repos))]
except Exception:
    stats = []

try:
    c = requests.get(f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last", timeout=15).json()
    days = c["contributions"]
    total = sum(x["count"] for x in days)
except Exception:
    days, total = [], 0

# ---------- Card 1: GitHub ----------
card((240, 120, 900, 580))
d.text((275, 150), "GitHub", font=font(26), fill=MUTED)
d.text((275, 190), f"@{USER}", font=font(52, True), fill=TEXT)
if stats:
    for i, (label, val) in enumerate(stats):
        y = 290 + i * 62
        d.text((275, y), label, font=font(30), fill=MUTED)
        d.text((865, y), str(val), font=font(34, True), fill=ACCENT, anchor="ra")
else:
    d.text((275, 300), "Couldn't reach GitHub", font=font(30), fill=MUTED)

# ---------- Card 2: To-do ----------
card((940, 120, 1480, 580))
d.text((975, 150), "To do", font=font(46, True), fill=TEXT)
try:
    with open(TODO, encoding="utf-8") as f:
        items = [l.strip() for l in f if l.strip()]
except FileNotFoundError:
    items = []
if not items:
    items = ["Nothing yet - add lines to todo.txt"]
for i, line in enumerate(items[:8]):
    done = line.startswith("x ")
    label = line[2:] if done else line
    y = 230 + i * 44
    box = (975, y + 6, 997, y + 28)
    
    if done:
        d.rounded_rectangle(box, radius=6, fill=ACCENT)
    else:
        d.rounded_rectangle(box, radius=6, outline=MUTED, width=2)
        
    fnt = font(28)
    d.text((1015, y), fit(label, fnt, 430), font=fnt, fill=MUTED if done else TEXT)

# ---------- Card 3: Calendar ----------
card((1520, 120, 1880, 580))
today = datetime.date.today()
d.text((1550, 150), today.strftime("%B %Y"), font=font(38, True), fill=TEXT)
for col, name in enumerate("MTWTFSS"):
    d.text((1550 + col * 46 + 23, 232), name, font=font(24), fill=ACCENT, anchor="mm")
for row, week in enumerate(calendar.monthcalendar(today.year, today.month)):
    for col, day in enumerate(week):
        if day == 0:
            continue
        cx, cy = 1550 + col * 46 + 23, 285 + row * 48
        if day == today.day:
            d.ellipse((cx - 21, cy - 21, cx + 21, cy + 21), fill=ACCENT)
        d.text((cx, cy), str(day), font=font(25),
               fill=BG if day == today.day else TEXT, anchor="mm")

# ---------- Card 4: contribution heatmap ----------
card((240, 620, 1880, 930))
d.text((275, 645), f"{total} contributions in the last year", font=font(30, True), fill=TEXT)
if days:
    first = datetime.date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7          # weeks start on Sunday
    x0, y0, size, gap = 275, 710, 22, 6
    for i, day in enumerate(days):
        pos = i + offset
        col, row = pos // 7, pos % 7
        x, y = x0 + col * (size + gap), y0 + row * (size + gap)
        d.rounded_rectangle((x, y, x + size, y + size), radius=5, fill=LEVELS[day["level"]])
else:
    d.text((275, 720), "Contribution data unavailable", font=font(28), fill=MUTED)

img.save(OUT)

# ---------- Set as wallpaper (Windows) ----------
import ctypes
ctypes.windll.user32.SystemParametersInfoW(20, 0, OUT, 3)