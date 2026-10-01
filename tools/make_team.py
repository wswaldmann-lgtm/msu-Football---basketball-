#!/usr/bin/env python3
"""Build another school's copy of the game tracker from the MSU app.

    python3 tools/make_team.py wmu          # reads teams/wmu.json, writes wmu/

The MSU app (index.html at the repo root) is the master copy. This script swaps in
the other team's schedules, colors, names, scores feeds and links, so every fix made
to the MSU app reaches the other teams the next time this runs (the Netlify build
runs it on every deploy). The other teams' apps have no fight-song intro.
"""
import datetime as dt
import html
import json
import os
import re
import shutil
import sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = ZoneInfo("America/Detroit")
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
DAYS = "Mon Tue Wed Thu Fri Sat Sun".split()

problems = []


def swap(page, old, new, count=None, required=True):
    """Replace text in the page; note it if the MSU app no longer contains it."""
    n = page.count(old)
    if n == 0:
        if required:
            problems.append(f"not found: {old[:70]!r}")
        return page
    if count is not None and n != count:
        problems.append(f"expected {count}x, found {n}x: {old[:70]!r}")
    return page.replace(old, new)


def iso(game, default_time):
    """Start time as ISO with the right Eastern offset (handles daylight saving)."""
    t = game["time"] if game["time"] != "TBA" else default_time
    clock = dt.datetime.strptime(t, "%I:%M %p").time()
    d = dt.date.fromisoformat(game["date"])
    return dt.datetime.combine(d, clock, TZ).isoformat()


def card(g, sport, team):
    d = dt.date.fromisoformat(g["date"])
    loc = g["loc"]
    star = ' data-star="1"' if g.get("star") else ""
    prefix = {"away": "at ", "neutral": "vs "}.get(loc, "")
    opp = html.escape(prefix + g["opp"]) + (" ⭐" if g.get("star") else "")
    when = "Time TBA" if g["time"] == "TBA" else g["time"]
    tv = g.get("tv", "")
    tv_html = ""
    if tv:
        tv_html = f' <span class="{"watch-tag" if tv.endswith("+") else "tv-tag"}">{html.escape(tv)}</span>'
    meta = f'{when}{" &middot;" + tv_html if tv_html else ""} &middot; {html.escape(g["where"])}'
    result = ""
    if g.get("result"):
        cls = "win" if g["result"].startswith("W") else "loss"
        result = f'\n        <div class="game-result {cls}">Final: {html.escape(g["result"])}</div>'
    badge = {"home": "Home", "away": "Away", "neutral": "Neutral"}[loc]
    info = [f"{'🏟 Home at' if loc == 'home' else '📍'} {html.escape(g['where'])}."]
    info.append(f"TV: {html.escape(tv)}." if tv else "TV and streaming are usually announced 1–2 weeks before the game.")
    if g["time"] == "TBA":
        info.append("Start time not announced yet.")
    if g.get("note"):
        info.append(html.escape(g["note"]))
    links = "\n".join(
        f'        <a class="mini-link" href="{u}" target="_blank" rel="noopener" onclick="event.stopPropagation()">{html.escape(label)}</a>'
        for label, u in team["links"][sport])
    default_time = "3:30 PM" if sport == "football" else "7:00 PM"
    return f'''
  <div class="game-card" data-loc="{loc}"{star} data-date="{iso(g, default_time)}" onclick="toggleCard(this)">
    <div class="game-main">
      <div class="game-date"><div class="month">{MONTHS[d.month - 1]}</div><div class="day">{d.day}</div><div class="weekday">{DAYS[d.weekday()]}</div></div>
      <div class="game-divider {loc}"></div>
      <div class="game-info">
        <div class="game-opponent">{opp}</div>
        <div class="game-meta">{meta}</div>{result}
      </div>
      <div class="game-badge badge-{loc}">{badge}</div>
      <div class="game-chevron">▼</div>
    </div>
    <div class="game-detail"><div class="detail-inner">
      <div class="detail-section">
        <div class="detail-label">📋 Game Info</div>
        <div class="detail-text">{" ".join(info)}</div>
      </div>
      <div class="link-row">
{links}
      </div>
    </div></div>
  </div>
'''


def section(sport, team, msu_section):
    """Keep the MSU scoreboard, rankings and calendar cards; replace record, outlook and games."""
    emoji = "🏈" if sport == "football" else "🏀"
    s = team[sport]
    head = msu_section[:msu_section.index('<div class="record-tracker">')]
    cal = re.search(r'\s*<div class="cal-card".*?\n  </div>\n', msu_section, re.S).group(0)
    rec = s["record"]
    record = f'''<div class="record-tracker">
    <div class="record-item"><div class="num w">{rec["w"]}</div><div class="lbl">Wins</div></div>
    <div class="record-sep">–</div>
    <div class="record-item"><div class="num l">{rec["l"]}</div><div class="lbl">Losses</div></div>
    <div class="record-item" style="margin-left:.75rem;padding-left:1.25rem;border-left:1px solid var(--border)">
      <div class="num" style="color:var(--gold-accent)">{rec["conf"]}</div><div class="lbl">{team["standings"]["label"]}</div>
    </div>
  </div>
'''
    games = "".join(card(g, sport, team) for g in s["games"])
    post = f'''
  <div class="season-outlook" style="margin-top:.5rem">
    <h3>{emoji} Postseason</h3>
    <div class="outlook-text">{s["postseason"]}</div>
  </div>
'''
    return head + record + cal + f"\n  <!-- {sport.upper()} -->" + games + post + "\n"


def build(slug):
    with open(os.path.join(ROOT, "teams", f"{slug}.json"), encoding="utf-8") as f:
        team = json.load(f)
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        page = f.read()
    c, short, nick = team["colors"], team["short"], team["nick"]

    # --- the schedules
    for sport in ("football", "basketball"):
        opener = f'<div id="{sport}" class="section' + (' active">' if sport == "football" else '">')
        start = page.index(opener) + len(opener)
        end = page.index(f"</div><!-- end {sport} -->")
        page = page[:start] + "\n" + section(sport, team, page[start:end]) + page[end:]

    # --- old-address redirect and banner are MSU-only
    page = re.sub(r"<script>\n// The app's home is now spartans-gameday.*?</script>\n", "", page, count=1, flags=re.S)
    page = re.sub(r'<div id="movedBanner".*?</div>\n<script>if \(window.__movedBanner\).*?</script>\n', "", page, count=1, flags=re.S)
    page = swap(page, "localStorage.getItem('msu_installed')||window.__movedBanner", "localStorage.getItem('msu_installed')")

    # --- no fight-song intro for other teams
    page = re.sub(r'\s*<button class="mode-toggle" onclick="toggleSound\(\)"[^\n]*</button>', "", page, count=1)
    page = swap(page, "function soundOn() { try { return localStorage.getItem('msu_sound') !== 'off'; } catch (e) { return true; } }",
                "function soundOn() { return false; }  // no intro music for this team (yet)")
    page = swap(page, " The fight song plays (🔊 in the top bar mutes it).", "")
    page = re.sub(r"\s*<li><b>🔊 / 🔇</b>[^\n]*</li>", "", page, count=1)

    # --- colors
    for old, new in [
        ("--spartan-green:#18453B;", f"--spartan-green:{c['primary']};"),
        ("--spartan-green-dark:#0F2B24;", f"--spartan-green-dark:{c['primaryDark']};"),
        ("--spartan-green-light:#1E5A4C;", f"--spartan-green-light:{c['primaryLight']};"),
        ("--gold-accent:#C5A551;", f"--gold-accent:{c['accent']};"),
        ('<meta name="theme-color" content="#18453B">', f'<meta name="theme-color" content="{c["primary"]}">'),
    ]:
        page = swap(page, old, new)
    page = page.replace("rgba(24,69,59,", f"rgba({c['primaryRgb']},")
    page = page.replace("rgba(46,125,95,", f"rgba({c['darkBadgeRgb']},")
    page = page.replace("#5BBF97", c["darkText"]).replace("#2E7D5F", c["darkDivider"]).replace("#06120e", c["splashBg"])

    # --- names and wording
    for old, new in [
        ('<meta name="apple-mobile-web-app-title" content="Spartans">', f'<meta name="apple-mobile-web-app-title" content="{team["homeTitle"]}">'),
        ("Spartans Game Tracker", team["appName"]),
        ("Unofficial fan app &middot; Go Green", f"Unofficial fan app &middot; {team['cheer'].rstrip('!')}"),
        ("Go Green!", team["cheer"]),
        ("💚", team["heart"]),
        ("made by a Spartan fan", f"made by a {team['nickSingular']} fan"),
        ("Not affiliated with Michigan State University", f"Not affiliated with {team['university']}"),
        ("Tap ↻ to load the latest MSU score", f"Tap ↻ to load the latest {short} score"),
        ("loads the latest MSU score", f"loads the latest {short} score"),
        ("or the Big Ten standings. MSU's row is highlighted", f"or the {team['standings']['label']} standings. {short}'s row is highlighted"),
        ('until MSU vs…', f"until {short} vs…"),
        (">B1G Standings<", f">{team['standings']['tabLabel']}<"),
        ("Big Ten &middot; Conf / Overall", f"{team['standings']['label']} &middot; Conf / Overall"),
        ("MSU not currently ranked in the ", f"{short} not currently ranked in the "),
        ("' until MSU '", f"' until {short} '"),
        ("'MSU ' + where", f"'{short} ' + where"),
        ("'Spartans').replace", f"'{nick}').replace"),
        ("MSU Watch Party", f"{short} Watch Party"),
        ("MSU TAILGATE", f"{short} TAILGATE"),
        ("Spartans Gameday project", f"{nick} Gameday project"),
        ("https://spartans-gameday.netlify.app", team["site"]),
        ("'msu-' + kind + '.ics'", f"'{team['slug']}-' + kind + '.ics'"),
    ]:
        page = swap(page, old, new)

    # --- ESPN feeds: team id and conference standings
    page = swap(page, "/teams/127/schedule", f"/teams/{team['espnId']}/schedule", count=2)
    page = swap(page, "college-football/standings?group=5'", f"college-football/standings?group={team['standings']['football']}'")
    page = swap(page, "mens-college-basketball/standings?group=7'", f"mens-college-basketball/standings?group={team['standings']['basketball']}'")
    page = swap(page, "t.team?.abbreviation === 'MSU'", f"t.team?.abbreviation === '{short}'")
    page = page.replace("/Michigan State/i", f"/{team['school']}/i")

    # --- trash talk
    lines = ",\n".join("  " + json.dumps(l, ensure_ascii=False) for l in team["trashTalk"])
    page, n = re.subn(r"const trashLines = \[.*?\n\];", "const trashLines = [\n" + lines + "\n];", page, count=1, flags=re.S)
    if not n:
        problems.append("trash talk list not found")

    # --- anything MSU-only left over?
    for leftover in ["Michigan State", "Spartan Stadium", "Breslin", "Izzo", "Big Ten", "msuspartans.com", "lansingstatejournal"]:
        if leftover in page:
            problems.append(f"MSU text left in page: {leftover!r}")

    out = os.path.join(ROOT, slug)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)

    # manifest + service worker
    with open(os.path.join(ROOT, "manifest.webmanifest"), encoding="utf-8") as f:
        man = json.load(f)
    man.update(name=f"{team['appName']} (unofficial fan app)", short_name=team["homeTitle"],
               background_color=c["manifestBg"], theme_color=c["primary"])
    with open(os.path.join(out, "manifest.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=2, ensure_ascii=False)
    with open(os.path.join(ROOT, "sw.js"), encoding="utf-8") as f:
        sw = f.read().replace("msu-tracker-", f"{slug}-tracker-")
    with open(os.path.join(out, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw)
    if not os.path.isdir(os.path.join(out, "icons")):
        problems.append(f"{slug}/icons is missing (make it with tools/make_team_icons.py)")

    print(f"Built {slug}/index.html: {sum(len(team[s]['games']) for s in ('football', 'basketball'))} games")
    if problems:
        print("WARNING, check these spots:\n  " + "\n  ".join(problems))
    return not problems


if __name__ == "__main__":
    sys.exit(0 if build(sys.argv[1] if len(sys.argv) > 1 else "wmu") else 1)
