# Spartans Game Tracker

A free, unofficial fan app for Michigan State football and basketball: schedules, countdowns, live scores, rankings, tailgate plans and watch-party invites, all in one place on your phone.

**Open it:** https://spartans-gameday.netlify.app

---

## The basics

1. **Put it on your home screen** so it opens like a real app.
   - **iPhone:** open the link in Safari, tap **Share** (the square with the arrow), then **Add to Home Screen**.
   - **Android:** open the link in Chrome, tap **⋮**, then **Add to Home screen** or **Install app**.
2. **Tap in** from the start screen. The fight song plays; the 🔊 button at the top mutes it.
3. **Use the bar at the bottom:**

   | Button | What it does |
   |---|---|
   | 🏈 Football | Football schedule |
   | 🏀 Basketball | Basketball schedule |
   | ⚡ Next Game | Jumps to the next game and opens it |
   | 🍔 Tailgate / 📺 Watch Party | Tailgate planner on the football tab, watch-party invites on the basketball tab |
   | 🔥 Trash Talk | A one-liner for the group chat |

4. **Tap any game** to open its preview and details.
5. Tap **?** at the top of the app any time for the built-in guide.

---

## Everything in more detail

### 📅 Schedule & games
- The countdown at the top always shows the next game.
- Each game card shows the date, time, TV network and where to stream it. Tap it for the preview and prediction.
- Filter with **All Games**, **Home**, **Away** or **Marquee**. The progress bar and record box track the season.

### 🔴 Live scores & rankings
- The **Scoreboard** card loads the latest MSU score. Tap **↻** to refresh; it turns red while a game is live.
- **Rankings & Standings** opens the AP Top 25 or the Big Ten standings, with MSU highlighted.

### 📆 Add games to your calendar
Each sport has an **Add games to your calendar** card. Subscribe once (iPhone/Mac Calendar or Google Calendar) and new kickoff and tip-off times appear on their own as they're announced.

### 🍔 Tailgate planner (football)
1. On the football tab, tap **Tailgate** and pick a home game.
2. **Who's Coming?** Add names and how many each person brings. The headcount adds up at the bottom.
3. **Who's Bringing What?** Starts with the basics (burgers, buns, cooler, grill, chairs, cornhole). Check items off, edit them, add your own, and put a name next to each.
4. **Share Plan** turns the whole thing into one text for the crew.

The tailgate plan is saved on your phone only, so share it to keep everyone in the loop.

### 📺 Watch Party (basketball)
No tailgate for hoops, so throw a watch party at a bar or someone's house.

**Hosting one**
1. On the basketball tab, tap **Watch Party**.
2. Pick the game and fill in **where**, the **address**, the **meet time**, your name and an optional note ("wings half off").
3. Tap **Create & Send Invite** and text the link to your friends.

**What your friends see**
- They tap the link (no app or sign-up needed) and answer 🙌 **Meet you there** (with how many are coming), 🤔 **Maybe**, or 😞 **Can't make it**.
- They can change their answer any time, and there's a map button to the spot.

**Forwarding**
- Anyone can tap **Invite a friend** to pass the invite along.
- People who answer from a forwarded link show up as "Sue *via Dave*," so you can see how word spread.

**Keeping track**
- Your parties are listed at the bottom of the Watch Party screen with live counts ("4 coming · 1 maybe").
- **Who's coming** opens your host view with everyone's answers. You can remove an answer with ×; guests can't.

### 📣 Share Hype & 🔥 Trash Talk
- **Share Hype** writes a countdown message ("6 days until MSU vs…") and opens your phone's share menu.
- **Trash Talk** serves up a one-liner. 🎲 for another, 📋 to copy.

### ⚙️ Buttons at the top
**?** guide · **🔊/🔇** fight-song intro on/off · **🌙/☀️** dark mode · **✕** back to the start screen

### 🔒 Privacy
No accounts or sign-ups. The app counts how many phones open it using a random ID, with no names or personal info. Tailgate lists stay on your phone. Watch-party invites and answers are stored on the invite service so the host and guests can see them.

### 💚 Support
Free, ad-free, made by a Spartan fan. Tap **Chip in** near the top of the schedule, or **Support this app** at the bottom, to tip on Venmo (@Sparty-Tracker). The top strip can be hidden with ×; it comes back after two weeks, or two months after someone chips in.

*Unofficial fan app. Not affiliated with Michigan State University.*

---

## For the app owner: how it's run

**Main address: https://spartans-gameday.netlify.app** (Netlify project `spartans-gameday`, linked to this repo, base directory `stats`). Every push to `main` rebuilds it. [`stats/build.mjs`](stats/build.mjs) assembles the site:

| Address | What it is |
|---|---|
| `/` | The app (`index.html` from the repo root) |
| `/stats` | Visitor stats: opens per day, unique phones, top states |
| `/p/<party id>` | Watch-party invite pages |
| `/api/*` | Counter, watch parties and answers ([`stats/netlify/functions`](stats/netlify/functions)) |
| `/msu-football.ics`, `/msu-basketball.ics` | Calendar feeds, rebuilt from the schedule on every deploy |

**Old GitHub Pages address** (https://wswaldmann-lgtm.github.io/msu-Football---basketball-/) stays up, published by `.github/workflows/pages.yml`:
- Browser visits jump straight to the Netlify address.
- Phones that installed the old address see a banner asking them to re-add the app from the new one.
- Calendar subscriptions made at the old address keep working, since the `.ics` feeds are still published there.

**Fight-song intro:** synthesized in code (baritones and tubas) from the public-domain melody of "Victory for MSU" (F. I. Lankey, 1915). No audio file.

---

## Other teams (Western Michigan and future schools)

The MSU app is the master copy. Other schools get their own app made from it, so fixes to the MSU app reach every team on the next deploy.

| Team | Address | Settings |
|---|---|---|
| Western Michigan Broncos | https://wmu-gameday.netlify.app | [`teams/wmu.json`](teams/wmu.json) |

- **Schedules, colors, names, links, trash talk:** edit the team's file in [`teams/`](teams/). Time `"TBA"` means not announced; add `"result": "W 31–17"` after a game and update the `record`.
- **Build it:** `python3 tools/make_team.py wmu` writes `wmu/index.html` (the Netlify build runs this automatically). `python3 tools/make_team_icons.py wmu` makes the app icon and splash background (original artwork, no school logos).
- **Hosting:** each team is its own Netlify project linked to this repo with base directory `stats` and a `TEAM` environment variable (`wmu`). Each team keeps its own visitor stats (`/stats`) and watch-party invites.
- Other teams have no fight-song intro (yet).
- **Adding a school:** copy `teams/wmu.json`, change the details (ESPN team id, conference standings group), run the two scripts, and create a Netlify project with `TEAM` set to the new name.
