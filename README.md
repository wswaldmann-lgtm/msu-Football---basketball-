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
   | 🍔 Tailgate / 📺 Watch Party | Plan a tailgate or watch party and send invites (either sport) |
   | 🔥 Trash Talk | A one-liner for the group chat |

4. **Tap any game** to open its preview and details.
5. Tap **?** at the top of the app any time for the built-in guide.

The first time someone opens the app, a **quick tour** dims the screen and spotlights the real buttons one at a time (countdown, game cards, the bottom bar, **?**), with a shortcut to the party demo. It shows once per phone; **▶ Take the quick tour** at the top of the **?** guide replays it.

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

### 🎉 Watch parties & tailgates
New to it? Tap **▶ See how it works** at the top of the party screen (or in the **?** guide) for a 30-second demo that walks through hosting and what your friends see.

**Hosting one**
1. Tap **🍔 Tailgate** (football tab) or **📺 Watch Party** (basketball tab) in the bottom bar.
2. Pick **📺 Watch Party** or **🍔 Tailgate**, then the game (football or basketball).
3. **Where's the party?** Pick from the list:
   - 🏠 **My house** (type your address once; the app remembers it)
   - 🏡 **A friend's house** (whose, plus their address)
   - ⭐ **Our usual spots** (any spot you saved)
   - 🍺 **A bar near me** (lists the closest bars and pubs; tap one to fill it in)
   - 🅿️ **Stadium parking lot** (tailgates)
   - ➕ **Somewhere new** (check **Save as one of our usual spots** to keep it)
   An address is required so friends' maps go to the right place. Tap **📍 Here** to drop a map pin right where you're standing.
4. Add the meet time, your name and a note, then tap **Create & Send Invite** and pick your group text.
5. The **Your invite is ready** screen spells out what happens next and has **Send**, **Copy text** and **📅 My calendar** buttons.

**What your friends see**
- A link (no app or sign-up). A three-step strip at the top tells them how to answer: type a name, tap 🙌 **I'm in** (with how many), 🤔 **Maybe** or 😞 **Can't**, hit Send.
- Tailgate guests can say what they're bringing ("brats and a cooler"); it shows next to their name.
- After answering: **📅 Google Calendar** or **📅 iPhone / Outlook** to save it, and **📤 Invite a friend** to pass it on. Answers from a forwarded link show as "Sue *via Dave*."
- **Open in Maps** uses the map pin or address. With neither, it says to ask the host instead of guessing a city.

**Keeping track**
- Your parties are listed at the bottom of the party screen with live counts ("4 coming · 1 maybe").
- **Who's coming** opens your host view with everyone's answers (remove one with ×). **Send again** the day before works as a reminder.

**Tailgate food & gear checklist:** link at the bottom of the tailgate screen. Burgers, buns, cooler, grill, chairs, cornhole; check items off, add your own, put a name next to each, and **Share Plan** sends it as one text. Saved on your phone only.

### 📣 Share Hype & 🔥 Trash Talk
- **Share Hype** writes a countdown message ("6 days until MSU vs…") and opens your phone's share menu.
- **Trash Talk** serves up a one-liner. 🎲 for another, 📋 to copy.

### ⚙️ Buttons at the top
**?** guide · **🔊/🔇** fight-song intro on/off · **🌙/☀️** dark mode · **✕** back to the start screen

### 🔒 Privacy
No accounts or sign-ups. The app counts how many phones open it using a random ID, with no names or personal info. Your saved spots, home address and the tailgate checklist stay on your phone. Party invites (including the address or map pin) and answers are stored on the invite service so the host and guests can see them. **📍 Here** and **A bar near me** ask your phone for your location only when you tap them; nearby bars and street addresses come from OpenStreetMap.

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
| `/p/<party id>` | Party invite pages (watch parties and tailgates) |
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

### Florida schools

| Team | Address | Settings |
|---|---|---|
| UCF Knights | https://ucf-gameday.netlify.app | [`teams/ucf.json`](teams/ucf.json) |
| Florida State Seminoles | https://fsu-gameday.netlify.app | [`teams/fsu.json`](teams/fsu.json) |
| Florida Gators | https://uf-gameday.netlify.app | [`teams/uf.json`](teams/uf.json) |
| Miami Hurricanes | https://miami-gameday.netlify.app | [`teams/miami.json`](teams/miami.json) |
| USF Bulls | https://usf-gameday.netlify.app | [`teams/usf.json`](teams/usf.json) |
| FAU Owls | https://fau-gameday.netlify.app | [`teams/fau.json`](teams/fau.json) |
| FIU Panthers | https://fiu-gameday.netlify.app | [`teams/fiu.json`](teams/fiu.json) |

Optional settings: `schoolRegex` (exact pattern for the team's row when the plain name would match other schools, e.g. Miami vs. Miami (OH)), `colors.iconFg` (icon letter color when the accent is too dark), `monogram` (two letters on the icon).

### Netlify credits (free plan: 300 a month for the whole account)

Every production build costs **15 credits**, and if the account runs out, **every site goes offline until the month resets** (including non-tracker sites in the same account). Visitors cost very little (about 3 credits per 10,000 page loads, plus about 10 per GB of traffic).

- [`stats/ignore.mjs`](stats/ignore.mjs) makes each site rebuild only when files *it* uses changed: the MSU site for the root app, a team's site for its own folder or settings file. Changes to the shared server code or pages in `stats/` rebuild every linked site (9 × 15 = 135 credits), so batch those.
- Group several edits into one push instead of many small pushes.
- Check usage in Netlify under **Team settings → Usage & billing**.

