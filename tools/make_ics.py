#!/usr/bin/env python3
"""Build calendar files (.ics) from the game cards in index.html.

    python3 tools/make_ics.py            # writes msu-basketball.ics + msu-football.ics

The schedule lives in index.html only; this script reads it, so the calendar
can never disagree with the app. The Pages workflow runs it on every deploy.

Games with a published time become 2-hour events. Games whose time is still
"Time TBA"/"Time TBD" become all-day events titled "(time TBA)", and update
in subscribed calendars once the time is added to index.html.
"""
import datetime as dt
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "wswaldmann-lgtm.github.io"
PAGE = "https://wswaldmann-lgtm.github.io/msu-Football---basketball-/"

CARD = re.compile(
    r'<div class="game-card"[^>]*data-loc="(?P<loc>\w+)"[^>]*data-date="(?P<date>[^"]+)"'
    r'.*?<div class="game-opponent">(?P<opp>.*?)</div>'
    r'\s*<div class="game-meta">(?P<meta>.*?)</div>',
    re.S,
)


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).replace("⭐", "").strip()


def esc(value):
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def section(page, name):
    start = page.index(f'<div id="{name}"')
    end = page.index(f"<!-- end {name} -->", start)
    return page[start:end]


def build(page, name, label, emoji):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//MSU Spartans Game Tracker//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:MSU {label}",
        "X-WR-TIMEZONE:America/Detroit",
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
        "X-PUBLISHED-TTL:PT12H",
    ]
    count = 0
    for m in CARD.finditer(section(page, name)):
        start = dt.datetime.fromisoformat(m["date"])
        opp = text(m["opp"])
        meta = text(m["meta"])
        parts = [p.strip() for p in meta.split("·")]
        tba = parts[0].lower().startswith("time tb")
        where = parts[-1] if len(parts) > 1 else ""
        title = f"{emoji} MSU {opp if opp.startswith(('at ', 'vs ')) else 'vs ' + opp}"
        uid = f"msu-{name}-{start:%Y%m%d}@{HOST}"
        lines += ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp}"]
        if tba:
            day = start.date()
            lines += [
                f"DTSTART;VALUE=DATE:{day:%Y%m%d}",
                f"DTEND;VALUE=DATE:{day + dt.timedelta(days=1):%Y%m%d}",
                f"SUMMARY:{esc(title + ' (time TBA)')}",
                "TRANSP:TRANSPARENT",
            ]
        else:
            utc = start.astimezone(dt.timezone.utc)
            lines += [
                f"DTSTART:{utc:%Y%m%dT%H%M%SZ}",
                f"DTEND:{utc + dt.timedelta(hours=2):%Y%m%dT%H%M%SZ}",
                f"SUMMARY:{esc(title)}",
            ]
        if where:
            lines.append(f"LOCATION:{esc(where)}")
        lines += [f"DESCRIPTION:{esc(meta + chr(10) + PAGE)}", f"URL:{PAGE}", "END:VEVENT"]
        count += 1
    lines.append("END:VCALENDAR")
    # RFC 5545: CRLF line endings, lines folded at 75 octets
    return "\r\n".join(fold(l) for l in lines) + "\r\n", count


def fold(line):
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not out else 74):
            out.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    out.append(cur.decode("utf-8"))
    return "\r\n ".join(out)


def main():
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        page = f.read()
    for name, label, emoji in (("basketball", "Basketball", "🏀"), ("football", "Football", "🏈")):
        body, count = build(page, name, label, emoji)
        out = os.path.join(ROOT, f"msu-{name}.ics")
        with open(out, "w", encoding="utf-8", newline="") as f:
            f.write(body)
        print(f"{out}: {count} games")


if __name__ == "__main__":
    main()
